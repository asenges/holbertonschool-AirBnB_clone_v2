#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from os import environ as env
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base


class DBStorage():
    """This class manages storage of hbnb models with sqlalchemy ORM"""
    __engine = None
    __session = None

    def __init__(self):
        eng_creat = f'mysql+mysqldb://{env.get("HBNB_MYSQL_USER")}:\
{env.get("HBNB_MYSQL_PWD")}@\
{env.get("HBNB_MYSQL_HOST")}/{env.get("HBNB_MYSQL_DB")}'

        self.__engine = create_engine(eng_creat, pool_pre_ping=True)

        if env.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        res = {}
        if (not cls):
            for t in Base.__subclasses__():
                objs = self.__session.query(t).all()
                for item in objs:
                    res[f"{item.to_dict()['__class__']}.{item.id}"] = item
        else:
            if cls in Base.__subclasses__():
                objs = self.__session.query(cls).all()
                for item in objs:
                    res[f"{item.to_dict()['__class__']}.{item.id}"] = item

        return res

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to the data base"""
        self.__session.commit()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        Base.metadata.create_all(self.__engine)
        s_factory = sessionmaker(bind=self.__engine,
                                 expire_on_commit=False)
        Session = scoped_session(s_factory)

        self.__session = Session()

    def delete(self, obj=None):
        """
        delete obj from __objects if it’s inside
        if obj is equal to None, the method should not do anything
        """
        if (obj):
            try:
                key = "{}.{}".format(obj.to_dict()['__class__'], obj.id)
                self.__objects.pop(key)
                self.save()
            except Exception as Ex:
                pass

    def close(self):
        """Calls the __session.remove() method"""
        self.__session.remove()
