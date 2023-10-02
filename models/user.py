#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
import hashlib
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""



    def __setattr__(self, name, value):
        '''
            Set attribute for a User
        '''
        if name == 'password':
            pwhash = hashlib.md5(bytes(str(value), 'utf-8'))
            super().__setattr__(name, pwhash.hexdigest())
        else:
            super().__setattr__(name, value)
