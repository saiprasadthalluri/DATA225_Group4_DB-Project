SELECT Occupation, AVG(SM.SleepDuration) AS AvgSleepDuration
FROM person as P
JOIN SleepMetrics AS SM ON P.PersonID = SM.PersonID
GROUP BY Occupation;