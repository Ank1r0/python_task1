
from app.database.repository import Repository
from app.database.connection import ConnectionManager
from app.config.settings import AppSettings
db_mgr = ConnectionManager() 
repo_instance = Repository(db_mgr)

def help_command():
        print("list of currently available commands:")
        print("load -n rooms -p rooms.json")
        print("load -n students -p students.json")  


settings = AppSettings()

def orchestra(CommandResult):

    should_continue = True
    display_data = None
    target_format = settings.output_format

    if(CommandResult.action == "exit"):
        db_mgr.disconnect()
        return False, "Closing the app.","console"
    
    elif CommandResult.action == "output":
        msg = settings.set_format(CommandResult.out_format)
        return True, msg, "output changed." 
    
    elif(CommandResult.action == "load"):
        display_data = repo_instance.load(CommandResult.name,CommandResult.path)

    elif CommandResult.action == "ping":
        display_data = repo_instance.query_ping()

    elif(CommandResult.action == "query"): 
        display_data = repo_instance.query(CommandResult.query_id)
        return should_continue,display_data,settings.output_format

    elif(CommandResult.action == "help"):
        display_data = " "

    elif(CommandResult.action == "dataready"): 
        display_data = repo_instance.dataready() 


    return should_continue, display_data, "console"