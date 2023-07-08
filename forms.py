from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, FileField
from wtforms.validators import EqualTo, InputRequired,DataRequired,Regexp, Length, Email
from flask_wtf.file import FileAllowed


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Regexp(r'^\w+$', message="Username must contain only letters, digits, or underscores"),
        Regexp(r'^(?!.*\s)', message="Username cannot contain spaces")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=7, message="Password must be at least 7 characters long")
    ])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    brand = StringField('brand', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    size = TextAreaField('size', validators=[InputRequired()])
    price = TextAreaField('price', validators=[InputRequired()])
    image = FileField("image", validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField()