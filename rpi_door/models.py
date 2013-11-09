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


db_engine = create_engine(None, echo=True, pool_recycle=3600)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=True,
                                      expire_on_commit=False,
                                      bind=db_engine))

Base = declarative_base()
Base.query = session.query_property()


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    email = Column(Unicode(255))
    key_code_id = Column(Integer, ForeignKey("key_code.id"))
    key_code = relationship("KeyCode", backref="user")


class KeyCode(Base):
    __tablename__ = "key_code"

    id = Column(Integer, primary_key=True)
    code = Column(Unicode(26))


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
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
