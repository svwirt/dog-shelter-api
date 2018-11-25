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
from models.shelter import ShelterModel

class ShelterPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('zipcode',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @accept('application/json')
    def post(self):
        data = ShelterPost.parser.parse_args()
        name = data['name']
        if ShelterModel.find_by_name(data['name']):
            return {'message': "A shelter with name '{}' already exists.".format(name)}, 400

        str1 = "https://dog-shelter-api.herokuapp.com/"
        str2 = str1 + name
        shelter = ShelterModel(name, data['type'], data['zipcode'], str2)
        try:
            shelter.save_to_db()
        except:
            return {"message": "An error occurred creating the shelter."}, 500

        return shelter.json(), 201


class Shelter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('zipcode',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('shelter_self',
                        type=str,

                        )
    @accept('application/json')
    @jwt_required
    def get(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        shelter = ShelterModel.find_by_id(id)
        if shelter:
            return shelter.json()
        return {'message': 'Shelter not found'}, 404

    @accept('application/json')
    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        shelter = ShelterModel.find_by_id(id)
        if shelter:
            shelter.delete_from_db()
            return ('', 204)
        return {'message': 'Shelter not found.'}, 404

    @accept('application/json')
    @jwt_required
    def put(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Owner privilege required'}, 403
        data = Shelter.parser.parse_args()

        shelter = ShelterModel.find_by_id(id)
        name = data['name']
        str1 = "https://dog-shelter-api.herokuapp.com/"
        str2 = str1 + name
        if shelter:
            shelter.name = name
            shelter.type = data['type']
            shelter.zipcode = data['zipcode']
            shelter.shelter_self = str2
        else:
            shelter = ShelterModel(**data)

        shelter.save_to_db()

        return shelter.json()


class ShelterList(Resource):
    @accept('application/json')
    def get(self):
        return {'shelters': list(map(lambda x: x.json(), ShelterModel.query.limit(5).all()))}

class CleanupShelters(Resource):
    def delete(self):
        list(map(lambda x: x.delete_from_db(), ShelterModel.query.all()))
