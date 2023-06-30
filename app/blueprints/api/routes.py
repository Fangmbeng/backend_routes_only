from app.blueprints.authentication.auth import basic_auth, token_auth
from flask import Blueprint, request, jsonify
from models import db, User
from flask import request
from flask_login import login_required, current_user


api = Blueprint('api',__name__, url_prefix='/api')


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
def deletepost(user_id):
    user = User.query.get(user_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['username']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    user.delete()
    return user.to_dict(), 201