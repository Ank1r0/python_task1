# app/main.py
from app.commands.command_parser import command_parser
from app.orchestra import orchestra
from app.file_instruments.output import OutputHandler as output

def main():
    print("App is ready to use")
    print("Enter command 'help' print list of all available command.\n" \
    "The last section in help is an app intended flow, use those commands in order as written there to fully check app functionality.\n")

    is_running = True


    while is_running:
        input_command = input("> ")

        parsed_cmd = command_parser(input_command)
        
        # This returns the TUPLE (True/False, Data)
        is_running, data, current_format = orchestra(parsed_cmd)
        
        # Now we pass that data to our SOLID output handler
        output.display(data,current_format)

if __name__ == "__main__":
    main()