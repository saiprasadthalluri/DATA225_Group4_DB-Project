SELECT P.Gender, SM.SleepDuration, M.StressLevel
FROM Person AS P
JOIN SleepMetrics AS SM ON P.PersonID = SM.PersonID
JOIN Metrics AS M ON P.PersonID = M.PersonID
ORDER BY StressLevel
