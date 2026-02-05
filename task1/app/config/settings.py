class AppSettings:
    def __init__(self):
        # Default settings
        self.output_format = "console"
        self.output_folder = "exports"

    def set_format(self, new_format):
        valid_formats = ["xml", "json", "console"]
        if new_format in valid_formats:
            self.output_format = new_format
        else:
            raise ValueError("New format could not be applied")
