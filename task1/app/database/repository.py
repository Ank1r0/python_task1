from app.database.connection import ConnectionManager
import json
from app.file_instruments.input_checker import input_instrument
from app.file_instruments.sql_reader import SqlReader


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
        return "data ready flags has been changed to TRUE"

    def query_ping(self):
        """
        Ping the database to ensure the connection.
        """
        cursor = self.conn.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()

        if result:
            return "Server is working."
        return "Server is not responding."

    def load_db_structure_from_ddl(self, name, path):  # fixed
        print("load initiated.")
        cursor = self.conn.cursor()

        data, input_msg = input_instrument.read_json_s(path)

        if data is None:
            return input_msg

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
            except:
                return f"Error during loading {name}"
                success = False

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
            except:
                print(f"Error during loading {name}")
                success = False

            if success:
                self.students_loaded = True

        else:
            return f"The specified table with name: {name} cannot be loaded, load files possible only to 2 tables. 'rooms', 'students'."

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

        return f"data loaded, table {name}."

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
            print(f"Error during integrity check: {e}")
            return False

        finally:
            cursor.close()

    def query(self, prepQueryId):  # fixed

        if not self.checkFilesAndDb():
            return "Missing files or db, setup db and data first."

        print(f"EXECUTING QUERY {prepQueryId}")

        prepQuery = SqlReader.get_query_by_id(prepQueryId)

        if prepQuery is None:
            return f"Missing query ID."

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

        print("Index cretion initiated.")

        if not self.checkFilesAndDb():
            return "Missing files or db, setup db and data first."

        query = SqlReader.load_query("ensure_index.sql")
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            self.conn.commit()
            return "Index refreshed and created successfully."
        except Exception as e:
            return f"Database error during index creation: {e}"
