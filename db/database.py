import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


class Database:
    """Connection to the dabase set inside the .env file through a singleton instance."""

    _instance = None

    _connection = None

    def __new(cls):
        """Only one instance of the database is needed through the whole project.

        Returns:
            Database: Single instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None

        return cls._instance

    @property
    def connection(self):
        """Instance of the connection to the database. Opens it if it is not existant or has been closed.

        Returns:
            Connection: connection to the database.
        """
        if self._connection is None or self._connection.closed:
            self._connection = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                autocommit=True,
            )
        return self._connection

    def close(self):
        """Close the database connection if it is open and set the property to None."""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()

        self._connection = None
