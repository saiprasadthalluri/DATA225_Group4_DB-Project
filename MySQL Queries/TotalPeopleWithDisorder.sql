SELECT 
  P.Occupation AS Occupation,
  COUNT(*) AS TotalPeopleWithDisorder
FROM
  Person P
JOIN
  Metrics M ON P.PersonID = M.PersonID
JOIN
  SleepMetrics SM ON P.PersonID = SM.PersonID
JOIN
  PhysicalActivity PA ON P.PersonID = PA.PersonID
WHERE
  SM.SleepDisorder != 'None'
GROUP BY
  P.Occupation;
