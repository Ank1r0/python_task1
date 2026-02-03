USE somedb;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Student]') AND type in (N'U'))   
    BEGIN
        CREATE TABLE Student(
        birthdate date  NOT NULL,
        id int  PRIMARY KEY NOT NULL,
        fullname NVARCHAR(50)  NOT NULL,
        room int  NOT NULL,
        sex nvarchar(1)  NOT NULL);
    END
ELSE
    TRUNCATE TABLE Student;

