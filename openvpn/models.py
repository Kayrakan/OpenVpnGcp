from openvpn import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Projects():
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    project_name = db.Column(db.String(300), unique=True)

class Instances():
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    instance_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
