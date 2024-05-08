SELECT
	CASE
		WHEN Age >= 20 AND Age < 30 THEN '20-29'
        WHEN Age >= 30 AND Age < 40 THEN '30-39'
        WHEN Age >= 40 AND Age < 50 THEN '40-49'
        ELSE '50+'
	END AS AgeGroup,
    SUM(CASE WHEN SleepDisorder = 'Insomnia' THEN 1 ELSE 0 END) AS Insomnia,
    SUM(CASE WHEN SleepDisorder = 'Sleep Apnea' THEN 1 ELSE 0 END) AS SleepApnea,
    SUM(CASE WHEN SleepDisorder = 'None' THEN 1 ELSE 0 END) AS None
FROM Person AS P
JOIN SleepMetrics AS SM ON P.PersonID = SM.PersonID
GROUP BY AgeGroup;
