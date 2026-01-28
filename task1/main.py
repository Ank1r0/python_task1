#smth
from app.commands.command_parser import command_parser
from app.orchestra import orchestra
def main():

    print("App is ready to use")
    print("Enter the command, use -help to list all the commands.\nTo have a fully operating app use the command load")
    print("Hint, the command load is used to populate 2 main tables, 'rooms' and 'students'\nExample of usage: load -n rooms -p filepath/rooms.json\n")

    is_running = True


    while is_running:
        input_command = input()
        is_running = orchestra(command_parser(input_command))

        


if __name__ == "__main__":
    main()