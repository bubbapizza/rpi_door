from sqlalchemy import engine_from_config
from contextlib import contextmanager


###### GENERIC DATABASE WRAPPER #######

class database():
   """This is a wrapper class for SQLAlchemy databases.  It makes it 
      easier to do atomic transactions using a 'with' statement."""

   def __init__(self, **kwargs):
      """Initialize the database engine."""

      self.engine = engine_from_config(kwargs, echo=False)
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
