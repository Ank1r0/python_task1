from app.database.connection import ConnectionManager
import json
from app.file_instruments.input_checker import input_instrument
from app.file_instruments.sql_reader import SqlReader
from app.file_instruments.logger_setup import get_logger

logger = get_logger(__name__)


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

    def load_db_structure_from_ddl(self, name, path):
        cursor = self.conn.cursor()

        data = input_instrument.read_json_s(path)

        """INIT DB CHECKS ID DB IS EXISTS, IF NOT CREATE"""
        cursor.execute(SqlReader.load_query("init_db.sql"))
        cursor.execute(SqlReader.load_query("drop_constraint.sql"))

        if name == "rooms":
            cursor.execute(SqlReader.load_query("init_rooms.sql"))

            sql = "INSERT INTO ROOM (id, RoomName) VALUES (?, ?)"

            success = True
            try:
                for entry in data:
                    # Pass values as a tuple to prevent SQL injection
                    cursor.execute(sql, (entry["id"], entry["name"]))
            except Exception as e:
                logger.exception(f"Insert {name} into database failed. {e}")
                success = False
                return False

            if success:
                self.rooms_loaded = True

        elif name == "students":

            cursor.execute(SqlReader.load_query("init_students.sql"))

            sql = "INSERT INTO Student (birthdate,id,fullname,room,sex) VALUES (?, ?, ?, ?, ?)"

            success = True
            try:
                for entry in data:
                    cursor.execute(
                        sql,
                        (
                            entry["birthday"],
                            entry["id"],
                            entry["name"],
                            entry["room"],
                            entry["sex"],
                        ),
                    )
            except Exception as e:
                logger.exception(f"Insert {name} into database failed. {e}")
                success = False

            if success:
                self.students_loaded = True

        else:
            return f"Predefined tables only."  # ?

        if self.rooms_loaded & self.students_loaded:

            cursor.execute(SqlReader.load_query("add_constraint.sql"))

            self.ready_to_use = True

        self.conn.commit()
        print(f"Loading {name} functions finished succesfully.")

        print(f"table room: {self.rooms_loaded}")
        print(f"table student: {self.students_loaded}")
        print(f"overall ready: {self.ready_to_use}")

        if not self.ready_to_use:
            print("The data is not ready to be queried.")
        else:
            print("The data is ready to be queried.")

        return True

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
            return False

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
            return False

        query = SqlReader.load_query("ensure_index.sql")
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Creating index failed. Error: {e}")
            return False
