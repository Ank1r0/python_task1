"""
AppSettings
Manages global application state and user preferences.

This class centralizes configuration settings, such as data export formats
and storage locations. By using setter methods with validation, it ensures
that the application remains in a consistent state and prevents invalid
configurations from propagating through the system.
"""


class AppSettings:
    def __init__(self):
        # Default settings
        self.output_format = "console"
        self.output_folder = "exports"

        """
        set_format
        Updates the global output strategy.
        
        Validates the requested format against supported types (xml, json, console).
        Raises a ValueError if the format is unsupported, protecting the 
        OutputHandler from processing undefined types.
        """

    def set_format(self, new_format):
        valid_formats = ["xml", "json", "console"]
        if new_format in valid_formats:
            self.output_format = new_format
        else:
            raise ValueError("New format could not be applied")
