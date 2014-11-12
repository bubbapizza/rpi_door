# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from helper import database


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
