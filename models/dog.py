from db import db
from flask import jsonify, render_template, request
from string import Template


class DogModel(db.Model):
    __tablename__ = 'dogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    breed = db.Column(db.String(80))
    dogSelf = db.Column(db.String(80))
    employee = db.Column(db.String(80))
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'))
    shelters = db.relationship('ShelterModel')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel', back_populates="dogs")


    def __init__(self, name, shelter_id, breed, dogSelf, employee):

        self.name = name
        self.shelter_id = shelter_id
        self.breed = breed
        self.dogSelf = dogSelf
        self.employee = employee

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'shelter id': self.shelter_id,
                'breed': self.breed,
                'self': self.dogSelf,
                'employee id': self.employee}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
