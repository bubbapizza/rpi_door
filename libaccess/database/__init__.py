from schema import User, KeyCode
import helper

####### GENERIC DOOR CONTROLLER DATABASE #######

class doorControllerDB(helper.database):
   """This class adds special functions to the SQL database."""
   
    def __init__(self):
        """The generic door controller database, just uses a SQL Alchemy
        memory database."""

        DATABASE_PARAMETERS = { "sqlalchemy.url": "sqlite:///" }
        super().__init__(DATABASE_PARAMETERS)
        

    def validate_key_code(self, data):
        key = self.connect().query\
                     .options(joinedload(KeyCode.user))\
                     .filter(KeyCode.code == data)\
                     .first()

        if key and (key.user and key.enabled):
            return True
        return False


    def create_user(self, data):
        """Create a user account.  You must pass a dictionary with
        the user column data."""

        user = User(**data)
        with self.transaction() as trans:
            trans.add(user)



####### SQLITE DATABASE #######

class localSQLite(doorControllerDB):
    """Creates a SQLite door controller database."""

    class __init__(self, filename):
        """All we need is the filename for a SQLite database."""

        DATABASE_PARAMETERS = {
            "sqlalchemy.url": "sqlite:///" + filename,
            "sqlalchemy.echo": False,
            "sqlalchemy.pool_recycle": 3600
        }
        
        super().__init__(DATABASE_PARAMETERS)


####### MYSQL DATABASE #######

class mySQL(doorControllerDB):
    """Creates a mySQL door controller database."""

    class __init__(self, 
                   user="root", 
                   passwd="password"
                   host="localhost", 
                   port=3389, 
                   dbname="doorcontrol"
                   ):
        """To initialize a mySQL database, we need hostname, TCP 
        port, and some user credentials."""

        DATABASE_PARAMETERS = {
            "sqlalchemy.url": "mysql://%s/%s@%s:%n/%s" % \
                (user, passwd, host, port, dbname)
        }
        
        super().__init__(DATABASE_PARAMETERS)

