USE somedb;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Student]') AND type in (N'U'))   
    BEGIN
        CREATE TABLE Student (
            id INT PRIMARY KEY,
            birthdate DATETIME2,    -- Use DATETIME2 for ISO dates from JSON
            fullname NVARCHAR(255), -- Use 255 to be safe for names
            room INT,
            sex CHAR(1)             -- This is fine for "M" or "F"
        );
    END
ELSE
    TRUNCATE TABLE Student;

