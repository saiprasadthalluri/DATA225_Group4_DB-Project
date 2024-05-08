SELECT
  Gender,
  CASE
    WHEN Age BETWEEN 20 AND 29 THEN '20-29'
    WHEN Age BETWEEN 30 AND 39 THEN '30-39'
    WHEN Age BETWEEN 40 AND 49 THEN '40-49'
    ELSE '50+'
  END AS AgeGroup,
  AVG(QualityOfSleep) AS AvgQualityOfSleep
FROM
  Person AS P
JOIN
  SleepMetrics AS SM ON P.PersonID = SM.PersonID
GROUP BY
  Gender, AgeGroup
ORDER BY
  Gender, AgeGroup;