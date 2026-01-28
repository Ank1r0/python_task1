
from app.database.repository import Repository
from app.database.connection import ConnectionManager

db_mgr = ConnectionManager() 
repo_instance = Repository(db_mgr)

def help_command():
        print("list of currently available commands:")
        print("load -n rooms -p rooms.json")
        print("load -n students -p students.json")  

def orchestra(CommandResult):

    should_continue = True
    display_data = None

    if(CommandResult.action == "exit"):
        db_mgr.disconnect()
        return False, "Closing the app."
    
    elif(CommandResult.action == "load"):
        display_data = repo_instance.load(CommandResult.name,CommandResult.path)

    elif CommandResult.action == "ping":
        display_data = repo_instance.query_ping()

    elif(CommandResult.action == "query"): 
        display_data = repo_instance.query(CommandResult.query_id)

    elif(CommandResult.action == "help"):
        display_data = "Some help text"

    elif(CommandResult.action == "dataready"): 
        display_data = repo_instance.dataready() 


    return should_continue, display_data