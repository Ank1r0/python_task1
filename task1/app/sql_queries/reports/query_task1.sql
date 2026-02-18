SELECT TOP 5 room,AVG(YEAR(GETDATE()) - YEAR(birthdate)) AS AverageAge FROM student
group by room
order by AVG(YEAR(GETDATE()) - YEAR(birthdate))