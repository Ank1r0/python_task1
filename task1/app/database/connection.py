import pyodbc
import os
from app.file_instruments.logger_setup import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    def __init__(self, conn_str=None):

        self.conn_str = conn_str
        self.congif = conn_str
        self.connection = None

        if conn_str is None:
            conn_str = os.getenv("DB_CONNECTION_STRING")
            if conn_str is None:
                raise ValueError("No connection")

        self.congif = conn_str
        self.connection = None
        self.connect()

    def connect(self):

        if not self.connection:
            # You MUST call the function with your config string here
            self.connection = pyodbc.connect(self.congif)
            self.connection.autocommit = True  # - just for testing purposes.
            print("Connected.")

        return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        print("Connection closed.")
