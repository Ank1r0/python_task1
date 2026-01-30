
# 1. Project Title & Overview

### Title: Python SQL Orchestra (PSO)

### Description: A console based application to interact with a MS SQL server via pyodbc.

### Tech Stack: Python 3.11, Docker

### Functionality: The project is made to execute the prepared queries.

List of prepared queries:

* List of rooms and the number of students in each of them

* 5 rooms with the smallest average age of students

* 5 rooms with the largest difference in the age of students

* List of rooms where different-sex students live

* List of rooms where same-sex students live (Extra)

  

# 2. Architecture & Design Principles
## Structure
├── app/
│   ├── commands/  
│	  │    └──`command_parser.py`  -- Parsing string into the command attributes
│   ├── config/         
│	  │    └── `settings.py` -- Stores the settings and function for their modification
│   ├── database/       
│	  │    ├── `connection.py` -- Connection manager( connect and disconnect )
│	  │    └── `repository.py` -- DB Interactions like: ping, query, etc.
│   ├── file_instruments/ 
│	  │    ├── `input_checker.py` -- Check the file's accesability and reads it.
│	  │    └── `output.py` -- Prints the data into the file.
│   └── `orchestra.py` --  Dispatcher, controls the flow
├── `main.py`             # Entry point, main cycle starts here.
└── Dockerfile
       
## Component level:
`command_parser.py` - works as a translation layer between the user and the system.
Consists of 2 primary parts: class `CommandResult` and function `command_parser`
### `Class CommandResult` :
the class has attributes like:

* Action - used to define the orchestra next step, (e.g. help - call the print help function, exit - ds and close the app)

* name, - used to define the name of the table during the load action

* path, - used to define the path to the file during the load action

* query_id, - define id of the prepquery during the query function

* out_format, - define the format that will be used during format change action
* msg - Currently used only for error message in case of failure

### `command_parser` :
Parsing function that validates string inputs and maps them to a `CommandResult` instance. It includes internal error handling to catch "Incomplete command structures" before they reach the database layer.
Has several 


# 3. Database Requirements

  
  

# 4. Getting Started (Usage)

  
  

# 5. Command List

  
  

# 6. Dockerization