"""This module has all the different libaccess database types."""

from schema import User, KeyCode
import helper


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
        

    def validate_key_code(self, data):
        key = self.connect().query\
                     .options(joinedload(KeyCode.user))\
                     .filter(KeyCode.code == data)\
                     .first()

        if key and (key.user and key.enabled):
            return True
        return False


####### SQLITE DATABASE #######

class SQLite(doorControllerDB):
    """Creates a SQLite door controller database."""

    def __init__(self, filename):
        """All we need is the filename for a SQLite database."""

        doorControllerDB.__init__(self, "sqlite:///" + filename,
            echo = False,
            pool_recycle = 3600
        )


####### MYSQL DATABASE #######

class mySQL(doorControllerDB):
    """Creates a mySQL door controller database."""

    def __init__(self, 
                 user="root", 
                 passwd="password",
                 host="localhost", 
                 port=3389, 
                 dbname="doorcontrol"
                 ):
         """To initialize a mySQL database, we need hostname, TCP 
         port, and some user credentials."""
 
         uri = "mysql://%s/%s@%s:%n/%s" % \
             (user, passwd, host, port, dbname)
         
         doorControllerDB.__init__(self, uri)
 
