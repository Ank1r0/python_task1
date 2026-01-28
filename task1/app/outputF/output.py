class OutputHandler:
    @staticmethod
    def display(data):
        if data is None:
            return
            
        if isinstance(data, list):
            # It's a database result (list of rows)
            print("\n--- QUERY RESULTS ---")
            for row in data:
                print(row)
            print("---------------------\n")
        else:
            # It's a simple message or help text
            print(data)