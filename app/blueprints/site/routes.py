from flask import Blueprint, render_template
from models import User, db, check_password_hash, Post
from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import LoginForm, PostForm

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required


site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/', methods = ['GET', 'POST'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = PostForm()
    if form.validate_on_submit():
        # Get data from form
        brand = form.brand.data
        name = form.name.data
        size = form.size.data
        price=form.price.data
        # Create new post instance which will also add to db
        new_post = Post(brand=brand, name=name, price=price, size=size, img=image, user_id=current_user.id)
        flash(f"{new_post.brand} has been created", "success")
        return redirect(url_for('site.index'))
        
    return render_template('create.html', form=form)