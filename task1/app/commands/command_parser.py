
class CommandResult: 
    def __init__(self,action,name=None,path=None,query_id=None,out_format=None,msg=None):
        self.action = action
        self.name = name
        self.path = path
        self.query_id = query_id
        self.out_format = out_format
        self.msg = msg
        

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
            if "-t" not in input_command:
                raise ValueError("Incomplete command structure")
            
            out_format = input_command[input_command.find("-t")+3:]

            if out_format is None:
                raise ValueError("Output format cannot be empty.")
                        
            return CommandResult(action="output",out_format=out_format)  
        except Exception as e:
            return CommandResult(
                action="internal_error",msg=str(e)
            )

    
    elif(input_command.find("load")== 0):      
        print("Load cmd parsing.")

        try:
            
            if "-n" not in input_command or "-p" not in input_command:
                raise ValueError("Incomplete command structure")

            name=(input_command[input_command.find("-n")+3:input_command.find("-p")-1])
            path=(input_command[input_command.find("-p")+3:])

            if name is None or path is None:
                raise ValueError("Name or Path cannot be empty")
            
            return CommandResult(action="load",name=name,path=path)
        
        except Exception as e:
            return CommandResult(
                action="internal_error",msg=str(e)
            )

    elif(input_command.find("query")== 0):
        print("Query cmd parsing")
        try:

            if "-id" not in input_command:
                raise ValueError("Incomplete command structure")
            
            query_id = int(input_command[input_command.find("-id")+3:])

            if query_id is None or query_id < 0:
                raise ValueError("Wrong id for a query.")

               
            return CommandResult(action="query",query_id=query_id)
        except Exception as e:
            return CommandResult(
                action="internal_error",msg=str(e)
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