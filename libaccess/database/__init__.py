from schema import *

####### SQLITE DATABASE #######

class localSQLite(database):
    """This is a a wrapper class for hiding the ugly details of
    SQL database access."""

    class __init__(self, filename):
        """All we need is the filename for a SQLite database."""

        DATABASE_PARAMETERS = {
            "sqlalchemy.url": "sqlite:///" + filename,
            "sqlalchemy.echo": False,
            "sqlalchemy.pool_recycle": 3600
        }
        
        super(database, self).__init__(DATABASE_PARAMETERS)

    def validate_key_code(self, data):
        """This is where we look up the key code for access."""

        raise NotImplementedError("Not implemented")
