SET NOCOUNT ON; 

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'somedb')
BEGIN
    USE somedb;

    IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[room]') AND type = 'U')
       AND EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[student]') AND type = 'U')
    BEGIN
        DECLARE @RoomCount INT = (SELECT COUNT(*) FROM [dbo].[room]);
        DECLARE @StudentCount INT = (SELECT COUNT(*) FROM [dbo].[student]);

        IF @RoomCount > 0 AND @StudentCount > 0
            SELECT 1 AS IsReady;
        ELSE
            SELECT 0 AS IsReady;
    END
    ELSE
        SELECT 0 AS IsReady;
END
ELSE
    SELECT 0 AS IsReady;