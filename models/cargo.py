from db import db


class CargoModel(db.Model):
    __tablename__ = 'cargos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    weight = db.Column(db.Float(precision=2))
    content = db.Column(db.String(80))
    delivery_date = db.Column(db.Integer)
    cargoSelf = db.Column(db.String(80))
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'))
    ship = db.relationship('ShipModel')
    # ships = db.relationship('ShipModel', lazy='dynamic')

    def __init__(self, name, weight, ship_id, content, delivery_date, cargoSelf):
        self.name = name
        self.weight = weight
        self.ship_id = ship_id
        self.content = content
        self.delivery_date = delivery_date
        self.cargoSelf = cargoSelf

    def json(self):
        return {'id': self.id, 'name': self.name, 'weight': self.weight, 'carrier': self.ship_id, 'content': self.content, 'delivery_date': self.delivery_date, 'self': self.cargoSelf}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
