import os


class SqlReader:
    @staticmethod
    def load_query(file_name):

        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "sql_queries/system", file_name)

        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"Error: SQL file {file_name} not found.")

    @staticmethod
    def get_query_by_id(query_id):

        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(
            base_path, f"sql_queries/reports/query_task{query_id}.sql"
        )

        try:
            with open(file_path, "r") as f:
                return f.read()
        except:
            raise ValueError(f"SQL file with a query number'{query_id}' not found.")
