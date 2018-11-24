from flask_restful import Resource, reqparse
from flask_jwt_extended import JWTManager
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
    get_raw_jwt
)
from flask_accept import accept
from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
_user_parser.add_argument('shelter_id',
                    type=int,

                    help="This field cannot be blank."
                    )
_user_parser.add_argument('status',
                    type=str,

                    help="This field cannot be blank."
                    )


class UserRegister(Resource):
    @accept('application/json')
    def post(self):
        data = _user_parser.parse_args()
        name = data['username']
        str1 = "https://dog-shelter-api.herokuapp.com/"
        str2 = str1 + name
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        s_id = None
        user = UserModel(name, data['password'], data['status'], s_id, str2)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    @accept('application/json')
    @jwt_required
    def get(cls, user_id):
        user =UserModel.find_by_id(user_id)
        if not user:
            return{'message': 'User not found'}, 404
        return user.json()

    @classmethod
    @accept('application/json')
    @jwt_required
    def delete(cls, user_id):
        user =UserModel.find_by_id(user_id)
        if not user:
            return{'message': 'User not found'}, 404
        user.delete_from_db()
        return ('', 204)

    @classmethod
    @accept('application/json')
    @jwt_required
    def put(cls, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        data = _user_parser.parse_args()
        user =UserModel.find_by_id(user_id)
        name = data['username']
        str1 = "https://dog-shelter-api.herokuapp.com/"
        str2 = str1 + name
        if user:
            user.username = name
            user.password = data['password']
            user.status = data['status']
            user.shelter_id = data['shelter_id']
            user.userSelf = str2
        else:
            user = UserModel(id, **data)

        user.save_to_db()

        return user.json()

class UserList(Resource):
    @accept('application/json')
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

class CleanupUsers(Resource):
    def delete(self):
        list(map(lambda x: x.delete_from_db(), UserModel.query.all()))

class UserLogin(Resource):
    @accept('application/json')
    def post(self):
        #get data from parse_args
        data = _user_parser.parse_args()
        # find user in databse
        user = UserModel.find_by_username(data['username'])
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity = user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @accept('application/json')
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200

class TokenRefresh(Resource):
    @accept('application/json')
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token= create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
