"""This module has all the different libaccess database types."""

from schema import User, KeyCode
import helper
import sqlalchemy


####### GENERIC DOOR CONTROLLER DATABASE #######

class doorControllerDB(helper.database):
    """This class adds special functions to the SQL database."""

    def __init__(self, uri=None, **kwargs):
        """The generic door controller database, just uses a SQL Alchemy
        memory database."""

        if not uri:
            helper.database.__init__(self, "sqlite:///", **kwargs)
        else:
            helper.database.__init__(self, uri, **kwargs)
        

    def validate_key_code(self, code):
        """Check the KeyCode table to make sure we have a user
        associated with the key and the key is enabled.  Return True
        or False depending on the result."""

        key = self.connect().query(KeyCode)\
                     .filter(KeyCode.code == code)\
                     .first()

        if key and (key.user and key.enabled):
            return True
        return False


####### SQLITE DATABASE #######

class SQLite(doorControllerDB):
    """Create and/or open a SQLite door controller database."""

    def __init__(self, filename):
        """All we need is the filename for a SQLite database."""

        doorControllerDB.__init__(self, "sqlite:///" + filename,
            echo = False,
            pool_recycle = 3600
        )


####### MYSQL DATABASE #######

class mySQL(doorControllerDB):
    """Create and/or open a mySQL door controller database."""

    def __init__(self, 
                 user="root", 
                 passwd="password",
                 host="localhost", 
                 port=3389, 
                 dbname="doorcontrol"
                 ):
         """To initialize a mySQL database, we need hostname, TCP 
         port, and some user credentials."""
 
         # Connect to the mySQL server and create the database if it
         # doesn't already exist.
         uri = "mysql://%s:%s@%s:%d" % \
             (user, passwd, host, port)
         engine = sqlalchemy.create_engine(uri)
         engine.execute("CREATE DATABASE IF NOT EXISTS %s;" % dbname)
         
         # Now that we know we have a database, connect to it and
         # create the schema if necessary.
         uri = "mysql://%s:%s@%s:%d/%s" % \
             (user, passwd, host, port, dbname)
         doorControllerDB.__init__(self, uri)
 
