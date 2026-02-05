select count(*) as StudentsInRoom, room from student
group by room
order by room