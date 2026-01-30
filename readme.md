
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
       

## 2.2 Component Architecture

### **Command Handling** (`app/commands/command_parser.py`)

This module acts as a translation layer between the raw CLI input and the internal system logic.

-   **`Class CommandResult`**: A data transfer object (DTO) that holds the "Intent" of the user.
    
    -   `action`: Determines the next step for the Dispatcher (e.g., `help`, `exit`, `load`).
        
    -   `name`: The target table name for data ingestion.
        
    -   `path`: The local file path for JSON data sources.
        
    -   `query_id`: The specific index of the prepared SQL query to be executed.
        
    -   `out_format`: The desired serialization format for results.
        
    -   `msg`: Stores error details in case of parsing failures.
        
-   **`function command_parser`**: Validates string inputs and maps them to a `CommandResult` instance. It prevents malformed commands from reaching the database layer.
    
    -   **Example**: `load -n rooms -p rooms.json` returns a result with `action="load"`, `name="rooms"`, and `path="rooms.json"`.
        

----------

### **Configuration Management** (`app/config/settings.py`)

Centralizes application state and environmental preferences.

-   **`Class AppSettings`**: Manages two primary attributes: `output_format` and `output_folder`.
    
-   **Output Formats**: Supports `console` (standard out), `JSON`, and `XML` file serialization.
    
-   **`set_format`**: A setter method triggered by the `output -t [format]` command to dynamically change how the application presents data.
    

----------

### **Database Layer** (`app/database/`)

Follows the **Repository Pattern** to separate data access from business logic.

#### **Connection Management** (`connection.py`)

-   **`Class ConnectionManager`**: Exclusively handles the lifecycle of the database socket.
    
-   **Attributes**: Stores the connection string in `config` and the active pyodbc object in `connection`.
    
-   **Methods**: Provides `connect()` and `disconnect()` to ensure resources are managed safely.
    

#### **Data Access Layer** (`repository.py`)

-   **`Class Repository`**: Abstracts the complexity of T-SQL operations.
    
-   **State Tracking**: Uses internal flags (`rooms_loaded`, `students_loaded`) to prevent queries on incomplete datasets.
    
-   **Relational Logic**: Manages database creation, table truncation, and the automatic application of **Foreign Key Constraints** once both datasets are loaded.
    
-   **Execution**: Maps user IDs to a list of **Prepared Queries**, transforming raw SQL rows into Python dictionaries for the output handlers.

**  "The Repository utilizes Dependency Injection, receiving an instance of ConnectionManager to ensure a clean separation between database connectivity and data manipulation logic."  **

#### **1. State Management (Flags)**

The repository tracks the "health" and "readiness" of the data through internal flags (`rooms_loaded`, `students_loaded`, `ready_to_use`). This ensures the app won't attempt to run complex queries until the schema is fully populated.

#### **2. Schema & Data Ingestion (`load`)**

The `load` function manages the entire lifecycle of the database tables:

-   **Dynamic Database Creation:** Automatically creates the `somedb` database if it doesn't exist.
    
-   **Idempotent Operations:** Uses "If Exists" checks and `TRUNCATE` logic so that loading data multiple times doesn't cause primary key crashes or duplicate records.
    
-   **Relational Integrity:** Automatically manages **Foreign Key Constraints** between Students and Rooms once both datasets are present.
    

#### **3. Prepared Query Execution (`query`)**

Instead of writing SQL in the UI, the repository uses a **Predefined Query List**.

-   **Input Safety:** Validates indices to prevent out-of-range errors.
    
-   **Data Mapping:** Uses a `zip` operation to transform raw SQL rows into Python dictionaries, making the data ready for the `OutputHandler` to convert to JSON or XML.
    

#### **4. Performance Optimization (`create_index`)**

Includes a dedicated method to manage a composite index (`room`, `birthdate`). This demonstrates an understanding of database performance tuning for large datasets.

### **File Instruments** (`app/file_instruments/`)

This layer handles the "Physical" boundary of the application—ensuring that external files are safely read and internal data is correctly serialized.

#### **Input Validation** (`input_checker.py`)

-   **`Class input_instrument`**: Implements defensive file-handling logic to prevent runtime crashes during data ingestion.
    
-   **Security & Integrity Checks**: Before attempting to read, the module verifies:
    
    -   **Path Existence**: Confirms the location is valid.
        
    -   **Object Type**: Ensures the target is a file, not a directory.
        
    -   **Extension Type**: Enforces `.json` strictness for the `load` action.
        
    -   **Permissions**: Checks OS-level read access (`R_OK`).
        
-   **Robust Parsing**: Uses a `try-except` block to handle corrupted JSON structures, returning clean error messages to the dispatcher.
    

#### **Output Management** (`output.py`)

-   **`Class OutputHandler`**: A polymorphic output service that transforms Python objects into user-readable formats.
    
-   **Format Versatility**:
    
    -   **JSON**: Serializes data using `json.dump` with clean indentation.
        
    -   **XML**: Dynamically builds an XML tree using `ElementTree`. It includes "cleaning" logic (converting spaces to underscores in tags) and uses `minidom` for high-quality "pretty-print" formatting.
        
    -   **Console**: A fallback for real-time debugging and simple messaging.
        
-   **Automatic Archiving**: Generates unique filenames using a `result_YYYYMMDD_HHMMSS` timestamp pattern to prevent users from accidentally overwriting previous query results.


### **Orchestration Layer** (`app/orchestra.py`)

The `orchestra` function serves as the application's **Command Dispatcher**. It centralizes the business logic to ensure the `main.py` remains clean and focused only on the loop.

-   **Service Mediation**: It acts as the bridge between the **Command Parser**, the **Repository**, and the **Output Handler**.
    
-   **Dynamic Routing**: It evaluates the `CommandResult.action` and routes the request to the appropriate method (e.g., calling `repo.load()` or `repo.query()`).
    
-   **Format Coordination**: It dynamically switches between `console`, `json`, and `xml` formats based on global `AppSettings`.
    
-   **User Guidance**: Includes a built-in `help_command` that provides a detailed manual of CLI syntax and the intended workflow order.

### **Main Loop** (`main.py`)

This file manages the application lifecycle and the **Infinite Command Loop**.

-   **Connection Guard**: Before starting, it enforces a security check. It prompts the user for a connection preference and terminates the process immediately if a database link cannot be established.
-   **Cycle Management**: Implements the **Read-Parse-Execute-Display** cycle. It keeps the application state alive until the `orchestra` signals a shutdown via the `is_running` flag.    
-   **SOLID Implementation**: Notice that `main.py` never talks to the SQL driver directly; it delegates all technical work to the specialized managers.

**Recommended Testing Flow:**

1.  `ping` — Check server health.
    
2.  `load -n rooms -p rooms.json` — Initialize database and rooms.
    
3.  `load -n students -p students.json` — Populate students and link Foreign Keys.
    
4.  `index` — Optimize the database.
    
5.  `output -t xml` — Switch to XML mode.
    
6.  `query -id 0` — Execute the first prepared query and check the generated `.xml` file.

# 3. Database Requirements
  This application is specifically designed for **Microsoft SQL Server**. It utilizes **T-SQL** features (like `IF EXISTS` and `sys.indexes`) and requires the **Microsoft ODBC Driver 18**.

-   **Database Engine:** MS SQL Server 2019 or later.
    
-   **ODBC Driver:** [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server). (Note: This is automatically installed inside the provided Docker image).
    
-   **Network:** Port **1434** (or your mapped SQL port) must be open and accessible.

# 4. Getting Started (Usage)
### **Step 1: Start your SQL Server**
If you are using Docker for the database, ensure your SQL Server container is running. Example command: 
`docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=SuperSafe_Pass99" -p 1434:1433 --name mssql -d mcr.microsoft.com/mssql/server:2022-latest`
  ### **Step 2: Installation**

**Option A: Using Docker (Recommended)** This avoids the need to install ODBC drivers manually on your host machine.
`docker build -t python-task1 .`
`docker run -it --network="host" --name my-app python-task1`

### **Step 3: Establishing the Connection**

Upon startup, the app will ask for a connection.

-   **Default:** Uses a hardcoded local configuration.
    
-   **Custom:** Use the following format for your connection string:
    
    > `DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost,1434;DATABASE=master;UID=sa;PWD=SuperSafe_Pass99;Encrypt=no;TrustServerCertificate=yes`

# 5. Technical Specifications

  **Requirement**

**Version / Value**

**Python**

3.11+

**Primary Library**

`pyodbc`

**Data Formats**

JSON (Input), JSON/XML/Console (Output)

**Container Base**

`python:3.11-slim` (Debian Bookworm)

**Database Driver**

`msodbcsql18`
  
