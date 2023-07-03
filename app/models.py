import os

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    last_names = Column(String(100))
    username = Column(String(100), unique=True)
    password_hash = Column(String(100))
    email = Column(String(100), unique=True)
    address = Column(String(100))
    phone = Column(String(100), unique=True)
    ordersServ = relationship("OrderServ", backref="owner", lazy = "dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User {}>".format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class OrderServ(db.Model):

    __tablename__="ordersServ"

    id = Column(Integer, primary_key=True)
    typeService = Column(String(100))
    timeRegister = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return "<orderServ {}>".format(self.id)


class OrderWork(db.Model):

    __tablename__= "ordersWork"

    id = Column(Integer, primary_key=True)
    typeWork = Column(String(100))
    budget = Column(String(6))
    workDuration = Column(String(3))
    technician = Column(String(100))
    timeRegister = Column(DateTime, default=datetime.utcnow)

