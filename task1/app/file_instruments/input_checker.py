import os
import json

"""
Utility class for robust file system interactions and data ingestion.

Acts as a defensive layer that validates file existence, integrity, and 
permissions before allowing the application to occupy memory with external 
data. This prevents 'Silent Failures' where an app might crash deep inside 
a logic loop due to a missing or inaccessible file.
"""

class input_instrument:

    @staticmethod
    def read_json_s(path):

        if not os.path.exists(path):
            raise ValueError("Path doesn't exist.")

        elif not os.path.isfile(path):
            raise ValueError("This object is not a file.")

        elif not path.lower().endswith(".json"):
            raise ValueError("This file is not json.")

        elif not os.access(path, os.R_OK):
            raise ValueError("The file is not readable.")

        with open(path, "r") as f:
            data = json.load(f)
        return data
