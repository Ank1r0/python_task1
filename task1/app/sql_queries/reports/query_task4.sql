SELECT room,COUNT(DISTINCT sex) as GenderDiversity
FROM student
GROUP BY room
HAVING COUNT(DISTINCT sex) = 1
order by room