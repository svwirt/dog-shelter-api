from db import db
from models.dog import DogModel


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    status = db.Column(db.String(80))
    userSelf = db.Column(db.String(80))
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'))
    shelters = db.relationship('ShelterModel', back_populates="users")
    dogs = db.relationship('DogModel', back_populates="users", lazy='dynamic')

    def __init__(self, username, password, status, shelter_id, userSelf):
        self.username = username
        self.password = password
        self.status = status
        self.shelter_id = shelter_id
        self.userSelf = userSelf

    def json(self):
        return{
            'id': self.id,
            'username': self.username,
            'status': self.status,
            'dogs': [dog.json() for dog in DogModel.find_all()],
            'shelter id': self.shelter_id,
            'self': self.userSelf
        }

    def dogOwner(self):
        return self.username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
