SELECT 
  P.Occupation,
  COUNT(*) AS TotalPeople,
  SUM(CASE WHEN SM.SleepDisorder IN ('Insomnia', 'Sleep Apnea') THEN 1 ELSE 0 END) AS SleepDisorderCount,
  ROUND(AVG(CASE WHEN SM.SleepDisorder IN ('Insomnia', 'Sleep Apnea') THEN 1 ELSE 0 END) * 100, 2) AS SleepDisorderPercentage
FROM
  Person P
JOIN
  Metrics M ON P.PersonID = M.PersonID
JOIN
  SleepMetrics SM ON P.PersonID = SM.PersonID
JOIN
  PhysicalActivity PA ON P.PersonID = PA.PersonID
GROUP BY
  P.Occupation
HAVING
  SleepDisorderCount > (
    SELECT AVG(SleepDisorderCount)
    FROM (
      SELECT Occupation, COUNT(*) AS SleepDisorderCount
      FROM Person P
      JOIN SleepMetrics SM ON P.PersonID = SM.PersonID
      WHERE SM.SleepDisorder IN ('Insomnia', 'Sleep Apnea')
      GROUP BY Occupation
    ) AS subquery
  )
ORDER BY
  SleepDisorderPercentage DESC;
