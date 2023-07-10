from app.blueprints.authentication.auth import basic_auth, token_auth
from flask import Blueprint, request, jsonify
from models import User, Post, Chart
from forms import PostForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user


api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Get data from form
        image = form.image.data
        brand = form.brand.data
        name = form.name.data
        size = form.size.data
        price = form.price.data
        #Create new post instance which will also add to db
        new_post = Post(brand=brand, name=name, size=size, price=price, img=image, user_id=current_user.id)
        flash(f"{new_post.brand} has been created", "success")
        return redirect(url_for('site.index'))
        
    return render_template('create.html', form=form)

@api.route('/posts/<int:post_id>')
@login_required
def get_post(post_id):
    # post = Post.query.get_or_404(post_id)
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    return render_template('post.html', post=post)


@api.route('/posts/<post_id>/edit', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('site.index'))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        image = form.image.data
        brand = form.brand.data
        name = form.name.data
        size = form.size.data
        price = form.price.data
        # update the post using the .update method
        post.update(brand=brand, name=name, size=size, price=price, img=image, user_id=current_user.id)
        flash(f"{post.brand} has been updated!", "success")
        return redirect(url_for('api.get_post', post_id=post.id))
    if request.method == 'GET':
        form.brand.data = post.brand
        form.name.data = post.name
        form.size.data =post.size
        form.price.data =post.price
        form.image.data =post.img
    return render_template('edit.html', post=post, form=form)

# DELETE car ENDPOINT

@api.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('site.index'))
    post.delete()
    flash(f"{post.brand} has been deleted", "info")
    return redirect(url_for('site.index'))



#API routes

@api.route('/token')
@basic_auth.login_required
def index_():
    user = basic_auth.current_user()
    token = user.get_token()
    return {'token':token, 'token_expiration':user.token_expiration}

@api.route('/users')
@token_auth.login_required
def get_user():
    user = token_auth.current_user()
    id = user.get_user_id()
    return {'id': id}

@api.route('/avatar')
@token_auth.login_required
def getavatar():
    user = token_auth.current_user()
    avatar = user.get_avatar()
    return {'avatar': avatar}
    

@api.route('/users', methods=['POST'])
def createuser():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['email', 'username', 'password']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    email = data.get('email')
    username = data.get("username")
    password = data.get('password')
            # Query our user table to see if there are any users with either username or email from form
    check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        # If the query comes back with any results
    if check_user:
        return ('A user with that email and/or username already exists.'), 400
    new_user = User(email=email, password=password, username= username)
    return new_user.to_dict(), 201
    
@api.route('/user/edit/<int:user_id>', methods=['POST'])
@token_auth.login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['username'] or ['email'] or ['password'] or ['avatar']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    username = data.get('username')
    password = data.get("password")
    email = data.get("email")
    avatar = data.get('avatar')
    same_user =  token_auth.current_user()
    if field == 'username':
        user.update(username=username, user_id=same_user)
        return user.to_dict()
    elif field == 'email':
        user.update(email=email, user_id=same_user)
        return user.dict()
    elif field == 'password':
        user.update(password=password, user_id=same_user)
        return user.dict()
    elif field == 'avatar':
        user.update(avatar = avatar, user_id=same_user)
        return user.dict()


@api.route('/user/delete/<int:user_id>', methods=['POST'])
@token_auth.login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['username']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    user.delete()
    return user.to_dict(), 201

@api.route('/posts', methods=['GET'])
def getposts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@api.route('/post/<int:post_id>')
def getpost(post_id):
    posts = Post.query.get(post_id)
    return posts.to_dict()

@api.route('/posts', methods=['POST'])
def createpost():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ["brand", "name", 'size', "price", "image"]:
        if field not in data:
            return(f"error:{field} must be in request body"), 400
    brand = data.get('brand')
    name=data.get('name')
    size = data.get("size")
    price=data.get('price')
    img= data.get('image')
    user =  token_auth.current_user()
    new_post = Post(brand=brand, name=name, price=price, size=size, img=img, user_id=user)
    return new_post.to_dict(), 201
    
@api.route('/post/edit/<int:post_id>', methods=['POST'])
def editpost(post_id):
    post = Post.query.get(post_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['brand'] or ['name'] or ['size'] or ['prices'] or ['image']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    brand = data.get('brand')
    name=data.get('name')
    size = data.get("size")
    price=data.get('price')
    img= data.get('image')
    user =  token_auth.current_user()
    if field=='brand':
        return post.update(brand=brand, user_id=user)
    if field=='name':
        return post.update(name=name, user_id=user)
    if field=='price':
        return post.update(price=price, user_id=user)
    if field=='size':
        return post.update(size=size, user_id=user)
    if field=='image':
        return post.update(img=img, user_id=user)
    return post.to_dict(), 201


@api.route('/post/delete/<int:post_id>', methods=['POST'])
def deletepost(post_id):
    post = Post.query.get(post_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['brand', 'name', 'size', 'price', 'image']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    post.delete()
    return post.to_dict(), 201

@api.route('/cart', methods=['GET'])
def getitems():
    chart = Chart.query.all()
    return jsonify([c.to_dict() for c in chart])

@api.route('/chart<int:chart_id>', methods=['GET'])
def getitem(chart_id):
    chart = Chart.query.get(chart_id)
    return chart.to_dict()

@api.route('/chart/delete/<int:chart_id>', methods=['POST'])
def delete_item(chart_id):
    chart = Chart.query.get(chart_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['name', 'size', 'price']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    chart.delete()
    return chart.to_dict(), 201

@api.route('/chart/empty', methods=['POST'])
def empty_chart():
    chart = Chart.query.all()
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['name', 'size', 'price']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    chart.delete()
    return chart.to_dict(), 201

@api.route('/chart/create', methods=['POST'])
def create_chart():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ["size", "name", "price"]:
        if field not in data:
            return(f"error:{field} must be in request body"), 400
    name=data.get('name')
    size = data.get("size")
    price=data.get('price')
    user =  token_auth.current_user()
    new_chart = Chart(name=name, price=price, size=size, user_id=user)
    return new_chart.to_dict(), 201