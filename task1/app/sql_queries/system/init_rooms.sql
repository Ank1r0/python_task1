USE somedb;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Room]') AND type in (N'U'))   
    BEGIN
        CREATE TABLE Room(
        id int PRIMARY KEY NOT NULL,
        RoomName nvarchar(15))
    END
ELSE
    TRUNCATE TABLE Room;


