from app.database.connection import ConnectionManager
import json
from app.file_instruments.input_checker import input_instrument
from app.file_instruments.sql_reader import SqlReader
from app.file_instruments.logger_setup import get_logger
import pyodbc

logger = get_logger("PyAppSQL.Repositpory:")

# --- CONFIGURATION (The only part you change) ---

"""
TABLE_CONFIG: Centralized Metadata Registry for Database Operations.

This dictionary serves as a dynamic mapping layer that decouples database 
logic from the Repository's execution methods. It allows the 'load' 
functionality to be extended to new tables without modifying core logic.

Key Features:
- SQL/JSON Mapping: Correlates JSON source keys with SQL destination columns.
- Type Safety: Uses 'input_sizes' to pre-allocate buffers and prevent 
  ODBC truncation errors.
- Data Transformation: 'cleaners' provide on-the-fly data sanitization 
  (e.g., ISO date trimming).
"""
TABLE_CONFIG = {
    "rooms": {
        "init_script": "init_rooms.sql",
        "sql": "INSERT INTO ROOM (id, RoomName) VALUES (?, ?)",
        "json_keys": ["id", "name"],
        # No special types needed for rooms, but we can be explicit
        "input_sizes": None,
        "db_name": "room",
    },
    "students": {
        "init_script": "init_students.sql",
        "sql": "INSERT INTO Student (birthdate, id, fullname, room, sex) VALUES (?, ?, ?, ?, ?)",
        "json_keys": ["birthday", "id", "name", "room", "sex"],
        # FIX 1: Explicitly tell SQL what data types to expect to prevent crashing
        "input_sizes": [
            (pyodbc.SQL_WVARCHAR, 50, 0),  # birthday (String -> Date)
            (pyodbc.SQL_INTEGER, 0, 0),  # id
            (pyodbc.SQL_WVARCHAR, 100, 0),  # name (Big buffer for long names)
            (pyodbc.SQL_INTEGER, 0, 0),  # room
            (pyodbc.SQL_CHAR, 1, 0),  # sex
        ],
        "db_name": "student",
        # FIX 2: Specific data cleaning rules
        "cleaners": {
            # Slice the first 19 chars of 'birthday' to remove ".000000"
            "birthday": lambda x: x[:19] if isinstance(x, str) else x
        },
    },
}


# ------------------------------------------------
class Repository:
    # Inside Repository class
    def __init__(self, ConnectionManager):
        self.mgr = ConnectionManager
        # .connect() returns the active connection object
        self.conn = self.mgr.connect()
        self.ready_to_use = False
        self.rooms_loaded = False
        self.students_loaded = False

    def dataready(self):
        self.ready_to_use = True
        self.rooms_loaded = True
        self.students_loaded = True
        return True

    def query_ping(self):
        """
        Ping the database to ensure the connection.
        """
        cursor = self.conn.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()

        if result:
            return True
        return False

    def load_experiment_not_safe(self, name, path):

        if name not in TABLE_CONFIG:
            raise ValueError(f"Table '{name}' is not defined in configuration.")

        config = TABLE_CONFIG[name]
        cursor = self.conn.cursor()

        # 1. Load JSON Data
        data = input_instrument.read_json_s(path)

        try:
            # 2. Run SQL Setup Scripts
            # Always run the base DB setup (idempotent checks usually inside the SQL)
            cursor.execute(SqlReader.load_query("init_db.sql"))
            cursor.execute(SqlReader.load_query("drop_constraint.sql"))
            cursor.execute(SqlReader.load_query(config["init_script"]))

            db_table_name = config["db_name"]
            logger.info(f"Wiping old data from table: {db_table_name}")

            # TRUNCATE is fast and resets the table completely
            cursor.execute(f"TRUNCATE TABLE {db_table_name}")

            # 3. Prepare Data Dynamically
            params = []
            cleaners = config.get("cleaners", {})

            for entry in data:
                row_values = []
                for key in config["json_keys"]:
                    raw_val = entry.get(key)

                    # Apply cleaner if one exists for this key (e.g., for 'birthday')
                    if key in cleaners:
                        raw_val = cleaners[key](raw_val)

                    row_values.append(raw_val)
                params.append(tuple(row_values))

            # 4. Execute Batch Insert (Optimized)
            if config["input_sizes"]:
                cursor.setinputsizes(config["input_sizes"])

            cursor.fast_executemany = True
            cursor.executemany(config["sql"], params)

            # 5. Update Loading Status Dynamically
            # Sets self.rooms_loaded = True (or students_loaded)
            setattr(self, f"{name}_loaded", True)

            # 6. Check if we can enable constraints
            # (Assuming you have these attributes initialized in __init__)
            if getattr(self, "rooms_loaded", False) and getattr(
                self, "students_loaded", False
            ):
                cursor.execute(SqlReader.load_query("add_constraint.sql"))
                self.ready_to_use = True
                print("[INFO] Relational integrity constraints enabled.")

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            logger.exception(f"Critical failure loading {name}")
            raise RuntimeError(f"Database load failed for {name}: {e}")

    def checkFilesAndDb(self):  # fixed
        query = SqlReader.load_query("check_db_integrity.sql")
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            while True:
                """traverse all query results and search for 1"""
                if cursor.description is not None:
                    row = cursor.fetchone()
                    if row and row[0] == 1:
                        self.ready_to_use = True
                        return True
                    break

                if not cursor.nextset():
                    break
            return False
        except Exception as e:
            logger.error(f"Error during integrity check: {e}")
            return False

        finally:
            cursor.close()

    def query(self, prepQueryId):  # fixed

        if not self.checkFilesAndDb():
            raise ValueError("Cannot interact with an empty database.")

        print(f"EXECUTING QUERY {prepQueryId}")

        prepQuery = SqlReader.get_query_by_id(prepQueryId)

        if prepQuery is None:
            return False

        cursor = self.conn.cursor()

        cursor.execute(prepQuery)

        columns = [column[0] for column in cursor.description]

        results = []
        for row in cursor.fetchall():
            """Combine column names with row values into a dictionary"""
            results.append(dict(zip(columns, row)))

        cursor.close()

        return results

    def create_index(self):  # fixed

        if not self.checkFilesAndDb():
            raise ValueError("Cannot create index in not prepared database.")

        query = SqlReader.load_query("ensure_index.sql")
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise ValueError(f"Creating index failed. Error: {e}")
