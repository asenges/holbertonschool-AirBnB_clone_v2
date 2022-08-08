#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ as env


if env.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine import db_storage
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    storage = file_storage.FileStorage()

storage.reload()
