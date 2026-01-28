
class CommandResult: 
    def __init__(self,action,name=None,path=None,query_id=None,out_format=None):
        self.action = action
        self.name = name
        self.path = path
        self.query_id = query_id
        self.out_format = out_format
        

def command_parser(input_command):
 
    if(input_command == "exit"):
        return CommandResult(action="exit")
    
    if(input_command == "index"):
        return CommandResult(action="index")
    
    if(input_command == "help"):
        return CommandResult(action="help")
    
    elif(input_command.find("output")== 0):      
        print("Output cmd parsing.")
        try:
            cmd = CommandResult(action="output",
                            out_format = input_command[input_command.find("-t")+3:])
            print(f"outputType: {cmd.out_format}")                 
            return cmd
        except Exception as e:
            return CommandResult(
                action="internal_error"
            )

    
    elif(input_command.find("load")== 0):      
        print("Load cmd parsing.")

        try:
            LoadResult = CommandResult(action="load",
                            name=(input_command[input_command.find("-n")+3:input_command.find("-p")-1]),
                            path=(input_command[input_command.find("-p")+3:]))
            return LoadResult
        except Exception as e:
            return CommandResult(
                action="internal_error"
            )

    elif(input_command.find("query")== 0):
        print("Query cmd parsing")
        try:
            queryRez = CommandResult(action="query",
                            query_id = int(input_command[input_command.find("-id")+3:]))
            print(f"query id: {queryRez.query_id}")                 
            return queryRez
        except Exception as e:
            return CommandResult(
                action="internal_error"
            )
    
    elif(input_command.find("ping")== 0):
        print("Ping cmd parsing")
        return CommandResult(action="ping")
    
    elif(input_command.find("dataready")== 0):
        print("ready data parsing")
        return CommandResult(action="dataready")
        
    else:
        print("Wrong command input, enter help if you need list of all available commands")
        return CommandResult(action="error")