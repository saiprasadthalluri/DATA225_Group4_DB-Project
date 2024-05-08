SELECT
  M.BMICategory,
  AVG(M.StressLevel) AS AvgStressLevel,
  AVG(SM.SleepDuration) AS AvgSleepDuration
FROM
  Metrics M
JOIN
  SleepMetrics SM ON M.PersonID = SM.PersonID
GROUP BY
  M.BMICategory
ORDER BY
  M.BMICategory;
