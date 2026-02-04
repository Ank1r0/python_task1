from app.database.repository import Repository
from app.database.connection import ConnectionManager
from app.config.settings import AppSettings
from app.file_instruments.logger_setup import get_logger

logger = get_logger(__name__)

Settings = AppSettings()


def help_command():
    print(
        "List of all available command:\n------------\n"
        "-load -n rooms -p rooms.json\n"
        "-load -n students -p students.json\n"
        "*The commands above used to load the data into the sql server, the database 'somedb' would be created after"
        "the first use of load and tables that we are trying to populate would be in this database.\n------------\n"
        "ping\n"
        "*command used to check is the database available.\n------------\n"
        "query -id 0\n"
        "*this command is used to execute the queries that are necessary based on the task.\n------------\n"
        "index\n"
        "*The command used to create a suggested index for necessary queries to speed up the query execution.\n------------\n"
        "output -t xml\n"
        "*the command used to define the queries output, by default the console is used, however there are 3 variants of output.\n"
        "xml - used to output the result queries into the XML files, json -  into the json, console - no files all data would be printed in console\n------------\n"
        "exit\n"
        "*command used to close the connection and terminate the app.\n------------\n"
        "dataready\n"
        "*command created for testing, using this command set up all flags that data and database is ready for execution.\n"
        "USE ONLY IF YOU SURE THAT DATA AND DATABASE EXISTS.\n\n"
        "Basic order or commands:\n"
        "ping\n"
        "load -n rooms -p rooms.json\n"
        "load -n students -p students.json\n"
        "index\n"
        "output -t xml\n"
        "query -id 0\n"
        "query -id 1\n"
        "exit\n"
    )


def orchestra(CommandResult, repo_instance, db_mgr):

    should_continue = True
    display_data = None

    try:
        if CommandResult.action == "exit":
            db_mgr.disconnect()
            return False, "Closing the app.", "console"

        elif CommandResult.action == "output":
            msg = Settings.set_format(CommandResult.out_format)
            return True, msg, "console"

        elif CommandResult.action == "load":
            display_data = repo_instance.load_db_structure_from_ddl(
                CommandResult.name, CommandResult.path
            )

        elif CommandResult.action == "ping":
            display_data = repo_instance.query_ping()

        elif CommandResult.action == "index":
            display_data = repo_instance.create_index()

        elif CommandResult.action == "query":
            display_data = repo_instance.query(CommandResult.query_id)
            return should_continue, display_data, Settings.output_format

        elif CommandResult.action == "help":
            help_command()
            display_data = ""

        elif CommandResult.action == "dataready":
            display_data = repo_instance.dataready()

        elif CommandResult.action == "internal_error":
            display_data = CommandResult.msg

        if display_data == False:
            display_data = "Error."
        elif display_data == True:
            display_data = "Done."

        return should_continue, display_data, "console"
    except Exception as e:
        # This catches EVERY error from every layer (File, DB, etc.)
        # We log it for the developer and show it to the user
        logger.error(f"Action failed: {e}")
        display_data = f"Error: {str(e)}"
