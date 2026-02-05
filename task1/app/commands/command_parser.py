import argparse
import shlex


"""
CommandResult
Data Transfer Object (DTO) for standardized command handling.
Represents the unified structure of any command entered by the user. 
By wrapping parsed arguments into this class, the Orchestra doesn't 
need to know about Argparse—it only deals with CommandResult objects.
"""


class CommandResult:
    def __init__(
        self,
        action=None,
        name=None,
        path=None,
        query_id=None,
        out_format=None,
    ):
        self.action = action
        self.name = name
        self.path = path
        self.query_id = query_id
        self.out_format = out_format


"""
argparse_instance
Configures the Command Line Interface (CLI) structure.
Defines all available subcommands (load, query, ping, etc.) and their required 
arguments. 'exit_on_error=False' is critical here so that a typo doesn't 
crash the entire application, but instead allows the parser to catch the error.
"""


def argparse_instance():
    parser = argparse.ArgumentParser(prog="MyTool", exit_on_error=False)

    subparsers = parser.add_subparsers(dest="command", required=True)

    load_parser = subparsers.add_parser("load")
    load_parser.add_argument("-n", "--name", required=True)
    load_parser.add_argument("-p", "--path", required=True)

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("-id", required=True, type=int)

    output_parser = subparsers.add_parser("output")
    output_parser.add_argument("-t", "--type", required=True)

    subparsers.add_parser("ping")
    subparsers.add_parser("index")
    subparsers.add_parser("dataready")
    subparsers.add_parser("help")
    subparsers.add_parser("exit")

    return parser


"""
command_parser
The logic bridge between raw user input and the application's Orchestra.
1. Uses 'shlex' to correctly split input strings (handling quoted paths).
2. Maps CLI-specific argument names (like 'id' or 'type') to the internal 
   CommandResult naming convention.
3. Returns a validated CommandResult object or raises a ValueError on failure.
"""


def command_parser(input_command):
    parser = argparse_instance()

    try:
        args_list = shlex.split(input_command)  # split by spaces between
        parsed = parser.parse_args(args_list)  # parsing into the parser

        args_dict = vars(parsed)  # Convert the argparse Namespace to a dictionary

        mapping = {
            "command": "action",
            "id": "query_id",
            "type": "out_format",
        }  # Rename keys if they don't match CommandResult exactly

        final_kwargs = {mapping.get(k, k): v for k, v in args_dict.items()}
        # used to rename mappings if they don't match, as an example command is action, the key should be renamed

        return CommandResult(**final_kwargs)  # ** autofilling

    except:
        raise ValueError("Wrong command.")
