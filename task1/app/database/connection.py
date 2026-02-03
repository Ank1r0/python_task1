import pyodbc
import os
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)


class ConnectionManager:
    def __init__(self, conn_str=None):

        self.conn_str = conn_str
        self.congif = conn_str
        self.connection = None

        try:
            if conn_str is None:
                conn_str = os.getenv("DB_CONNECTION_STRING")
                if conn_str is None:
                    raise ValueError("No connection")

            self.congif = conn_str
            self.connection = None
            self.connect()
        except Exception as e:
            logging.error(
                "Connection failed. The most common reason is a driver version. "
                f"Check your ODBC Driver version. P.S. Should be ODBC Driver 18 for SQL Server. "
                f"Error: {e}"
            )

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
