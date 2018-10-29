
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.cargo import CargoModel



class Cargo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('weight',
                        type=float,
                        # required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ship_id',
                        type=int,
                        required=True,
                        help="Every cargo needs a ship_id."
                        )
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('delivery_date',
                        type=int,
                        required=True,
                        help="Every cargo needs a ship_id."
                        )
    parser.add_argument('cargoSelf',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # @jwt_required()
    def get(self, id):
        cargo = CargoModel.find_by_id(id)
        if cargo:
            return cargo.json()
        return {'message': 'Cargo not found'}, 404

    def post(self, id):
        if CargoModel.find_by_id(id):
            return {'message': "An cargo with id '{}' already exists.".format(id)}, 400

        data = Cargo.parser.parse_args()

        cargo = CargoModel(id, **data)

        try:
            cargo.save_to_db()
        except:
            return {"message": "An error occurred inserting the cargo."}, 500

        return cargo.json(), 201

    def delete(self, id):
        cargo = CargoModel.find_by_id(id)
        if cargo:
            cargo.delete_from_db()
            return {'message': 'Cargo deleted.'}
        return {'message': 'Cargo not found.'}, 404

    def put(self, id):
        data = Cargo.parser.parse_args()

        cargo = CargoModel.find_by_id(id)

        if cargo:
            cargo.weight = data['weight']
            cargo.content = data['content']
            cargo.delivery_date= data['delivery_date']
            cargo.cargoSelf = data['cargoSelf']
        else:
            cargo = CargoModel(id, **data)

        cargo.save_to_db()

        return cargo.json()


class CargoList(Resource):
    def get(self):
        return {'cargos': list(map(lambda x: x.json(), CargoModel.query.all()))}
