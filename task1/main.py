# app/main.py
from app.commands.command_parser import command_parser
from app.orchestra import orchestra
from app.outputF.output import OutputHandler as output

def main():
    print("App is ready to use")
    print("Enter the command...")

    is_running = True

    while is_running:
        input_command = input("> ")

        parsed_cmd = command_parser(input_command)
        
        # This returns the TUPLE (True/False, Data)
        is_running, data = orchestra(parsed_cmd)
        
        # Now we pass that data to our SOLID output handler
        output.display(data)

if __name__ == "__main__":
    main()