from app.database.connection import ConnectionManager
import json
taskdb = 'somedb'

PrepQueries = ["""
        select count(*) as StudentsInRoom, room from student
        group by room
        order by room
        """,
        """
        select * from room
        where id = 23
        """]

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

        if(name == "rooms"):
            with open(path, 'r') as f:
                data = json.load(f)

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
            with open(path, 'r') as f:
                data = json.load(f)

        
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

        if(not self.checkFilesAndDb()):
            return "Missing files or db, setup db and data first."

        print(f"EXECUTING QUERY {PrepQueryId}")
         
        cursor = self.conn.cursor()
        
        cursor.execute(PrepQueries[PrepQueryId])

        return cursor.fetchall()
        
    
        

        

        
        
            