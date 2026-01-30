import pyodbc
taskdb = 'somedb'
class ConnectionManager:
    def __init__(self,conn_str = None):
        
        '''
        DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost,1434;DATABASE=master;UID=sa;PWD=SuperSafe_Pass99;Encrypt=no;TrustServerCertificate=yes
        '''

        self.conn_str = conn_str

        try:
            if conn_str is None:
                server = 'localhost'  # or '127.0.0.1'
                port = '1433'
                database = 'master'  # Default database
                username = 'sa'
                password = 'PASSword8'  # Your password
                driver = '{ODBC Driver 18 for SQL Server}'  # Most common
                
                # Connection string
                conn_str = f'DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes'

            self.congif = conn_str
            self.connection = None
            self.connect()
        except:
            print("Connection failed. The most common reason is a driver version. Check your ODBC Driver version. P.S. Should be ODBC Driver 18 for SQL Server.")
        

        

    def connect(self):
        if not self.connection:
            # You MUST call the function with your config string here
            self.connection = pyodbc.connect(self.congif) 
            self.connection.autocommit = True # - just for testing purposes.
            print("Connected.")

        return self.connection
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        print("Connection closed.")
        






    