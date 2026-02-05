IF EXISTS (
    SELECT 1 
    FROM sys.indexes 
    WHERE name = 'idx_student_room_birthdate' 
    AND object_id = OBJECT_ID('student')
)
BEGIN
    DROP INDEX idx_student_room_birthdate ON student;    
END
CREATE INDEX idx_student_room_birthdate 
ON student (room, birthdate);