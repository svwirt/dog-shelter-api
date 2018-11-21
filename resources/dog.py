from db import db
from flask_restful import Resource, reqparse
from flask_accept import accept
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.dog import DogModel
from models.user import UserModel


class DogPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int

                        )
    parser.add_argument('name',
                        type=str,

                        help="Name field cannot be left blank top!"
                        )
    parser.add_argument('shelter_id',
                        type=int,
                        required=True,
                        help="Every dog needs a shelter_id."
                        )
    parser.add_argument('breed',
                        type=str,

                        help="Breed field cannot be left blank!"
                        )
    parser.add_argument('dogSelf',
                        type=str,

                        help="Self field cannot be left blank!"
                        )
    parser.add_argument('employee',
                        type=str
                       )
    @jwt_required
    def post(self):
        data = DogPost.parser.parse_args()
        employee_id = get_jwt_identity()
        # data = Dog.parser.parse_args()
        name = data['name']
        str1 = "https://dog-shelter-api.herokuapp.com/"
        str2 = str1 + name
        id = data['id']
        if DogModel.find_by_name(name):
            return {'message': "An dog with name '{}' already exists.".format(name)}, 400



        dog = DogModel(name, data['shelter_id'], data['breed'], str2, employee_id)

        try:
            dog.save_to_db()
        except:
            return {"message": "An error occurred inserting the dog."}, 500

        return dog.json(), 201

class Dog(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int

                        )
    parser.add_argument('name',
                        type=str,

                        help="Name field cannot be left blank top!"
                        )
    parser.add_argument('shelter_id',
                        type=int,
                        required=True,
                        help="Every dog needs a shelter_id."
                        )
    parser.add_argument('breed',
                        type=str,

                        help="Breed field cannot be left blank!"
                        )
    parser.add_argument('dogSelf',
                        type=str,

                        help="Self field cannot be left blank!"
                        )
    parser.add_argument('employee',
                        type=str
                       )
    @jwt_required
    def get(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        dog = DogModel.find_by_id(id)
        if dog:
            return dog.json()
        return {'message': 'Dog not found'}, 404

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        dog = DogModel.find_by_id(id)
        if dog:
            dog.delete_from_db()
            return {'message': 'Dog deleted.'}
        return {'message': 'Dog not found.'}, 404

    def put(self, id):
        data = Dog.parser.parse_args()

        dog = DogModel.find_by_id(id)

        if dog:
            dog.name = data['name']
            dog.breed = data['breed']
            dog.dogSelf = data['dogSelf']
        else:
            dog = DogModel(id, data['name'], data['shelter_id'], data['breed'], data['delivery_date'], data['dogSelf'])

        dog.save_to_db()

        return dog.json()

class GetUserDogs(Resource):
    @jwt_required
    def get(self, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        user =UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return{'message': 'User not found'}, 404

class DogList(Resource):
    def get(self):
        return {'dogs': list(map(lambda x: x.json(), DogModel.query.all()))}