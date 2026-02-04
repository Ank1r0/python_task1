# app/main.py
from app.commands.command_parser import command_parser
from app.orchestra import orchestra
from app.file_instruments.output import OutputHandler as output
from app.database.connection import ConnectionManager
from app.database.repository import Repository
import os

from app.file_instruments.logger_setup import get_logger

logger = get_logger(__name__)


def main():
    print("App is ready to use")
    print(
        "Enter command 'help' print list of all available command.\n"
        "The last section in help is an app intended flow, use those commands in order as written there to fully check app functionality.\n"
    )

    db_mgr = None
    print(
        "--- Starting the Python App ---\nSql server was initiated, however do you prefer to connect to another server?."
    )

    try:
        conn_str = os.getenv("DB_CONNECTION_STRING")

        if conn_str:
            print("Environment variable found. Auto-connecting...")
            db_mgr = ConnectionManager(conn_str)
        else:
            choice = input("Use default connection? (y/n): ").lower()

            if choice == "n":
                custom_conn_str = input("Enter you custom connection string: ")
                db_mgr = ConnectionManager(custom_conn_str)
            else:
                db_mgr = ConnectionManager()

        repo = Repository(db_mgr)

    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        logger.error(f"Application failed to start: {e}")

    if db_mgr is None or not db_mgr.connection:
        print("Security: Connection could not be established. App closing for safety.")
        return  # Terminate the app before reaching the while loop

    is_running = True
    while is_running:
        try:
            input_command = input("> ").lower()

            parsed_cmd = command_parser(input_command)

            # This returns the TUPLE (True/False, Data)
            is_running, data, current_format = orchestra(parsed_cmd, repo, db_mgr)

            # Now we pass that data to our SOLID output handler
            output.display(data, current_format)
        except Exception as e:
            print(f"\n[APPLICATION ERROR]: {e}")
            logger.error(f"Error during command execution. {e}")


if __name__ == "__main__":
    main()
