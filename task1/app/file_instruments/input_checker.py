import os
import json

class input_instrument:

    @staticmethod
    def read_json_s(path):
        print("Input file check.")

        if (not os.path.exists):
            return None,"Path doesn't exist."
        
        elif (not os.path.isfile):
            return None,"This object is not a file."
        
        elif (not path.lower().endswith('.json')):
            return None,"This file is not json. For the load only json files are used."
        
        elif (not os.access(path,os.R_OK)):
            return None,"The file is not readable."
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return data,"File reading done succesfully."
        except:
            return None, f"Error: Unexpected file error: {e}"

              

    
