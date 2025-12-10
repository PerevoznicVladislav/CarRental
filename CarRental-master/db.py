from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyCustomError(Exception):
    def __init__(self, message="An error occurred"):
        super().__init__(message)


class DatabaseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = db  # Initialize db instance
        else:
            raise MyCustomError("DatabaseConnector instance already exists. Use DatabaseConnector.get_instance() to access the instance.")
        return cls._instance

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

