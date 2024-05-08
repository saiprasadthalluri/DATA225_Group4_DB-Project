SELECT Occupation,
		SUM(CASE WHEN BMICategory = 'Normal' THEN 1 ELSE 0 END) AS Normal,
        SUM(CASE WHEN BMICategory = 'Overweight' THEN 1 ELSE 0 END) AS Overweight,
        SUM(CASE WHEN BMICategory = 'Obese' THEN 1 ELSE 0 END) AS Obese
FROM Person AS P
JOIN Metrics AS M ON P.PersonID = M.PersonID
GROUP BY Occupation;
