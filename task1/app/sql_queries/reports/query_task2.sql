select top 5 room,MAX(YEAR(GETDATE()) - YEAR(birthdate)) - MIN(YEAR(GETDATE()) - YEAR(birthdate)) as AgeDifference,
MAX(YEAR(GETDATE()) - YEAR(birthdate)) as MaximalAge,
MIN(YEAR(GETDATE()) - YEAR(birthdate)) as MinimalAge
from student
group by room
order by MAX(YEAR(GETDATE()) - YEAR(birthdate)) - MIN(YEAR(GETDATE()) - YEAR(birthdate)) DESC