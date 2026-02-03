IF EXISTS (SELECT * FROM sys.objects WHERE name = 'Table_2_room' AND parent_object_id = OBJECT_ID('student'))
    BEGIN
        ALTER TABLE student DROP CONSTRAINT Table_2_room
    END