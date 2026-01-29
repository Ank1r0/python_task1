from app.database.connection import ConnectionManager
import json
from app.file_instruments.input_checker import input_instrument
taskdb = 'somedb'

PrepQueries = [
        #query - 1
        """
        select count(*) as StudentsInRoom, room from student
        group by room
        order by room
        """,
        #query - 2
        """
        SELECT TOP 5 room,AVG(YEAR(GETDATE()) - YEAR(birthdate)) AS AverageAge FROM student
        group by room
        order by AVG(YEAR(GETDATE()) - YEAR(birthdate))
        """,
        #query - 3
        """
        select top 5 room,MAX(YEAR(GETDATE()) - YEAR(birthdate)) - MIN(YEAR(GETDATE()) - YEAR(birthdate)) as AgeDifference,
        MAX(YEAR(GETDATE()) - YEAR(birthdate)) as MaximalAge,
        MIN(YEAR(GETDATE()) - YEAR(birthdate)) as MinimalAge
        from student
        group by room
        order by MAX(YEAR(GETDATE()) - YEAR(birthdate)) - MIN(YEAR(GETDATE()) - YEAR(birthdate)) DESC
        """,
        #query - 4
        """
        SELECT room,COUNT(DISTINCT sex) as GenderDiversity
        FROM student
        GROUP BY room
        HAVING COUNT(DISTINCT sex) > 1
        order by room
        """,
        #query - 5
        """
        SELECT room,COUNT(DISTINCT sex) as GenderDiversity
        FROM student
        GROUP BY room
        HAVING COUNT(DISTINCT sex) = 1
        order by room
        """,
        ]

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
              
        # Now self.conn is a real connection object, so .cursor() will work!
        cursor = self.conn.cursor() 

        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()

        if result:
            return "server is working" 
        return "server is not responding"
        
    def load(self,name,path):
        print("load initiated.")
        cursor = self.conn.cursor() 

        data,input_msg = input_instrument.read_json_s(path) #using own input check and read function

        if(data is None):
            return input_msg

        if(name == "rooms"):

            

            cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{taskdb}'")

            exists = cursor.fetchone() 
            
            
            if not(exists):
                cursor.execute(f"CREATE DATABASE {taskdb}")
            
            cursor.execute(f"use {taskdb}")


            cursor.execute("""
            IF EXISTS (SELECT * FROM sys.objects 
                    WHERE name = 'Table_2_room' AND parent_object_id = OBJECT_ID('student'))
            BEGIN
                ALTER TABLE student DROP CONSTRAINT Table_2_room
                PRINT 'Constraint Dropped'
            END
            ELSE
            BEGIN
                PRINT 'Constraint not found'
            END
            """)

            cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[room]') AND type in (N'U'))
            SELECT 1 ELSE SELECT 0
            """)

            result = cursor.fetchone() #EXIST - 1, DONT EXIST - 0
            if(result[0] == 0):
                                         
                cursor.execute(f"""CREATE TABLE Room(
                        id int PRIMARY KEY NOT NULL,
                        RoomName nvarchar(15)
                )
                """)   
                print("table room created")   

            cursor.execute("TRUNCATE TABLE Room")

            sql = "INSERT INTO ROOM (id, RoomName) VALUES (?, ?)"

            success = True
            try:
                for entry in data:
                    # Pass values as a tuple to prevent SQL injection
                    cursor.execute(sql, (entry['id'], entry['name']))
            except:
                print(f"Error during loading {name}")
                success = False

            if(success):
                self.rooms_loaded = True
            

        if(name == "students"):
       
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{taskdb}'")
  
            exists = cursor.fetchone()
            
            if not(exists):
                cursor.execute(f"CREATE DATABASE {taskdb}")
            
            cursor.execute(f"use {taskdb}")

            cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Student]') AND type in (N'U'))
            SELECT 1 ELSE SELECT 0
            """)

            result = cursor.fetchone() #EXIST - 1, DONT EXIST - 0
    
            if(result[0] == 0):                       
                cursor.execute(f"""CREATE TABLE student 
                            (
                            birthdate date  NOT NULL,
                            id int  PRIMARY KEY NOT NULL,
                            fullname NVARCHAR(50)  NOT NULL,
                            room int  NOT NULL,
                            sex nvarchar(1)  NOT NULL,
                            );
                    
                """)   
                print("table student created")   
            
            cursor.execute("TRUNCATE TABLE Student")

            sql = "INSERT INTO Student (birthdate,id,fullname,room,sex) VALUES (?, ?, ?, ?, ?)"

            success = True
            try:
                for entry in data:
                    # Pass values as a tuple to prevent SQL injection
                    cursor.execute(sql, (entry['birthday'], entry['id'], entry['name'], entry['room'], entry['sex']))
            except:
                print(f"Error during loading {name}")
                success = False

            if(success):
                self.students_loaded = True

                #ALTER TABLE student ADD CONSTRAINT Table_2_room
                #FOREIGN KEY (room)
                #REFERENCES room (id);

            if(self.rooms_loaded & self.students_loaded):
                
                cursor.execute("""
                ALTER TABLE student ADD CONSTRAINT Table_2_room
                FOREIGN KEY (room)
                REFERENCES room (id);
                """)

                self.ready_to_use = True


        self.conn.commit()
        print(f"Loading {name} functions finished succesfully.")

        if(self.rooms_loaded == True & self.students_loaded == True):
            self.ready_to_use = True


        print(f"table room: {self.rooms_loaded}")
        print(f"table student: {self.students_loaded}")
        print(f"overall ready: {self.ready_to_use}")
        
        if(not self.ready_to_use):
            print("The data is not ready to be queried.")        
        else:
            print("The data is ready to be queried.")

        return f"data loaded, table {name}."
            
    def checkFilesAndDb(self):
        
        cursor = self.conn.cursor()

        if(not self.ready_to_use):
            print("Database missing files, use load commands to populate the data.\n")
            return False
        
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{taskdb}'")

        exists = cursor.fetchone() 
        
        if not(exists):
            print("Database is not ready to use, missing prepared database, use load function to create a database with the data.")
            return False

        cursor.execute(f"use {taskdb}")

        return True

    

    def query(self,PrepQueryId):

        if PrepQueryId > len(PrepQueries):
            return f"No prepared query for this index. Current pref queries amount:0 - {len(PrepQueries) - 1}"

        if(not self.checkFilesAndDb()):
            return "Missing files or db, setup db and data first."

        print(f"EXECUTING QUERY {PrepQueryId}")
         
        cursor = self.conn.cursor()
        
        cursor.execute(PrepQueries[PrepQueryId])

        columns = [column[0] for column in cursor.description]
    
        results = []
        for row in cursor.fetchall():
            # Combine column names with row values into a dictionary
            results.append(dict(zip(columns, row)))
            
        cursor.close()

        return results
        
    def create_index(self):
        print("Index cretion initiated.")

        if(not self.checkFilesAndDb()):
            return "Missing files or db, setup db and data first."
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT name AS IndexName, 
            type_desc AS IndexType
        FROM sys.indexes 
        WHERE name = 'idx_student_room_birthdate' 
        AND object_id = OBJECT_ID('student');
        """)

        if(cursor.fetchone()):
            print("Cursor already exists and will be dropped.")
            cursor.execute("""drop index idx_student_room_birthdate on student""")

        cursor.execute("""
        CREATE INDEX idx_student_room_birthdate 
        ON student (room, birthdate);
        """)        
        return "index created."
        
    
        

        

        
        
            