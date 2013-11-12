#!/usr/bin/python
#
#        Copyright (C) 2013 Randy Topliffe, Shawn Wilson
#        randy???@who_knows_where.com
#        shawn@ch2a.ca
#
#        
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   This program was written by Randy Topliffe with comments added by
#   Shawn Wilson who was trying to understand what the heck Randy did.


#
# This is the SQL database that controls door access.  It uses
# SQL Alchemy to abstract away the actual database type.
#
# The database has two tables: user and keycode.  The user table acts
# as a header for a list of keycodes that can be associated with the
# user.  This allows for multiple forms of identification to be
# associated with the user.  This means the keycodes could be used to
# store the values of RFID cards, swipe cards, etc.
#


####### IMPORT PYTHON MODULES ########

from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
)
from sqlalchemy.orm import relationship, joinedload
from contextlib import contextmanager


# Use SQLite to store door accsess info.  I have no idea why pool_recyle 
# is required.
db_engine = create_engine("sqlite:///database.db",
                          echo=True, pool_recycle=3600)

# Open the SQL session, with some unknown variables.  I have no idea
# why any of these parameters are required.  Or if sessionmaker is 
# required for that matter.
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         expire_on_commit=False,
                                         bind=db_engine))

# This variable appears to be the base class for creating SQL Alchemy 
# tables.
Base = declarative_base()

# Here I guess we create a query or something.
Base.query = db_session.query_property()




# Use a context manager to handle tearing down the session????
@contextmanager
def session_context():
    yield
    db_session.remove()


class SQLAlchemyBinding():
    """I have no fucking idea why this is here or what it does."""

    def validate_key_code(self, data):
        with session_context():
            key = KeyCode.query\
                         .options(joinedload(KeyCode.user))\
                         .filter(KeyCode.code == data)\
                         .first()
            # do other stuff
            # push to redis??
            # log stuff
            if key:
                return True
            return False


########### WHAT THE HELL IS THIS FOR? #############

def init_db():
    Base.metadata.create_all(db_engine)


def drop_db():
    """
    It is a workaround for dropping all tables in sqlalchemy.
    """
    if db_engine is None:
        raise Exception
    conn = db_engine.connect()
    trans = conn.begin()
    inspector = engine.reflection.Inspector.from_engine(db_engine)
    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []

        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk['name']))
            t = Table(table_name, metadata, *fks)
            tbs.append(t)
            all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()



######## DATABASE TABLES ###########

class User(Base):
    """This is the SQL table that stores user accounts."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    email = Column(Unicode(255))
    key_code_id = Column(Integer, ForeignKey("key_code.id"))
    key_code = relationship("KeyCode", backref="user")


class KeyCode(Base):
    """This table stores the list of keycodes that are associated with
    the user.  Any one of these codes could (probably) be used to open
    a door or gain access to a secured area/device/etc."""

    __tablename__ = "key_code"

    id = Column(Integer, primary_key=True)
    code = Column(Unicode(26))


