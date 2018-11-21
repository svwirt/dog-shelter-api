
from db import db


class ShelterModel(db.Model):
    __tablename__ = 'shelters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    zipcode = db.Column(db.Float)
    shelter_self = db.Column(db.String(80))
    dogs = db.relationship('DogModel', lazy='dynamic')
    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, name, type, zipcode, shelter_self):
        self.name = name
        self.type = type
        self.zipcode = zipcode
        self.shelter_self = shelter_self


    def json(self):
        return {'id': self.id,
                'name': self.name,
                'type': self.type,
                'zipcode': self.zipcode,
                'dogs': [dog.json() for dog in self.dogs.all()],
                'employees': [user.json() for user in self.users.all()],
                "self": self.shelter_self}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
