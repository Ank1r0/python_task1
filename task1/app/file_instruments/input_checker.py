import os
import json


class input_instrument:

    @staticmethod
    def read_json_s(path):

        if not os.path.exists:
            raise ValueError("Path doesn't exist.")

        elif not os.path.isfile:
            raise ValueError("This object is not a file.")

        elif not path.lower().endswith(".json"):
            raise ValueError("This file is not json.")

        elif not os.access(path, os.R_OK):
            raise ValueError("The file is not readable.")

        with open(path, "r") as f:
            data = json.load(f)
        return data
