#!/usr/bin/python3
"""
Database storage for Airbnb clone v2
"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """  """
    __engine = None
    __session = None

    def __init__(self):
        """  """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """  """
        if cls is None:
            objs_query = self.__session.query(State).all()
            objs_query.extend(self.__session.query(City).all())
            objs_query.extend(self.__session.query(User).all())
            objs_query.extend(self.__session.query(Place).all())
            objs_query.extend(self.__session.query(Review).all())
            objs_query.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs_query = self.__session.query(cls)
        return {"{}.{}".format(type(objt).__name__, objt.id):
                objt for objt in objs_query}

    def new(self, obj):
        """  """
        self.__session.add(obj)

    def save(self):
        """  """
        self.__session.commit()

    def delete(self, obj=None):
        """  """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """  """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
                  expire_on_commit=False, bind=self.__engine))
        self.__session = Session()

    def close(self):
        self.__session.remove()
