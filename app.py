
from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT


from resources.cargo import Cargo, CargoList
from resources.ship import Ship, ShipList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Ship, '/ship/<string:name>')
api.add_resource(ShipList, '/ships')
api.add_resource(Cargo, '/cargo/<string:name>')
api.add_resource(CargoList, '/cargos')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
