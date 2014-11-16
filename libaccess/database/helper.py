from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


###### GENERIC DATABASE WRAPPER #######

class database(object):
   """This is a wrapper class for SQLAlchemy databases.  It makes it 
      easier to do atomic transactions using a 'with' statement."""

   def __init__(self, uri, **kwargs):
      """Initialize the database engine."""

      self.engine = create_engine(uri, **kwargs)
      self.genSession = sessionmaker(bind=self.engine)

      # Create the database if it doesn't already exist.
      Base.metadata.create_all(self.engine, checkfirst=True)


   def connect(self):
      """Return a sqlAlchemy database session for the GPS database."""

      return self.genSession()


   @contextmanager
   def transaction(self):
      """Provide a database transaction scope for db operations."""

      # Example usage:
      #
      # db = database()
      # with db.transaction() as trans:
      #     trans.add(myTableRecord(args...))

      session = self.connect()
      try:
         yield session
         session.commit()

      except Exception as error:
         session.rollback()
         raise error

      finally:
         session.close()
