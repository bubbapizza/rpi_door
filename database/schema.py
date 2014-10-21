# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from helper import database

#
# These parameters get passed to the database wrapper so SQLAlchemy 
# knows the physical parameters of how/where the data is stored.
# 
DATABASE_PARAMETERS = {
    "sqlalchemy.url": "sqlite:///database.db",
    "sqlalchemy.echo": False,
    "sqlalchemy.pool_recycle": 3600
}


####### AUTHENTICATION DATABASE #######

class dbAuth(database):
   """This is the authentication database for the door controller."""

   def __init__(self):
      """Initialize the authentication database."""
      
      super(database, self).__init__(DATABASE_PARAMETERS)


########## SCHEMA OBJECTS ###########

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    email = Column(Unicode(255), unique=True)
    key_code_id = Column(Integer, ForeignKey("key_code.id"))
    key_code = relationship("KeyCode", backref=backref("user", uselist=False))


class KeyCode(Base):
    __tablename__ = "key_code"

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, default=True)
    code = Column(Unicode(255), unique=True)
