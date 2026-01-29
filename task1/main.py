# app/main.py
from app.commands.command_parser import command_parser
from app.orchestra import orchestra
from app.file_instruments.output import OutputHandler as output
from app.database.connection import ConnectionManager
from app.database.repository import Repository

def main():
    print("App is ready to use")
    print("Enter command 'help' print list of all available command.\n" \
    "The last section in help is an app intended flow, use those commands in order as written there to fully check app functionality.\n")

    is_running = True

    print ("--- Starting the Python App ---")
    choice = input("Use default connection? (y/n): ").lower()
    
    if choice == 'n':
        custom_conn_str = input("Enter you custom connection string: ")
        db_mgr = ConnectionManager(custom_conn_str)
    else:
        db_mgr = ConnectionManager()

    if not db_mgr.connection:
        print("Security: Connection could not be established. App closing for safety.")
        return # Terminate the app before reaching the while loop

    repo = Repository(db_mgr)

    while is_running:
        input_command = input("> ").lower()

        parsed_cmd = command_parser(input_command)
        
        # This returns the TUPLE (True/False, Data)
        is_running, data, current_format = orchestra(parsed_cmd, repo, db_mgr)
        
        # Now we pass that data to our SOLID output handler
        output.display(data,current_format)

if __name__ == "__main__":
    main()