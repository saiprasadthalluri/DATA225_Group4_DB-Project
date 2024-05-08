from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
from google.cloud.exceptions import NotFound

client = bigquery.Client.from_service_account_json(r"C:\Users\manjo\OneDrive\Documents\Homework\DATA 225\Project Files\term-project-421603-b7001589537c.json")

datasets = list(client.list_datasets())

# Iterate over datasets and tables to get IDs
for dataset in datasets:
    dataset_id = dataset.dataset_id
    tables = list(client.list_tables(dataset.reference))
    for table in tables:
        table_id = table.table_id
        print(f'Dataset ID: {dataset_id}, Table ID: {table_id}')

view1_id = 'term-project-421603.Sleep_Health.AvgSleepbyGender'
query1 = """
SELECT Gender, AVG(`SleepDuration`) AS Avg_Sleep_Duration
FROM `term-project-421603.Sleep_Health.TransformedData`
GROUP BY Gender
"""

view2_id = 'term-project-421603.Sleep_Health.BMIvsAvgHeartRate'
query2 = """
SELECT `BMICategory`, AVG(`HeartRate`) AS Avg_Heart_Rate
FROM `term-project-421603.Sleep_Health.TransformedData`
GROUP BY `BMICategory`
"""

view3_id = 'term-project-421603.Sleep_Health.DisordersbyAgeGroup'
query3 = """
SELECT CASE
              WHEN Age >= 21 AND Age <= 30 THEN '21-30'
              WHEN Age >= 31 AND Age <= 40 THEN '31-40'
              WHEN Age >= 41 AND Age <= 50 THEN '41-50'
              ELSE '51+'
          END AS Age_Group,
          COUNTIF(`SleepDisorder` = 'Insomnia') AS Insomnia_Count,
          COUNTIF(`SleepDisorder` = 'Sleep Apnea') AS Sleep_Apnea_Count,
          COUNTIF(`SleepDisorder` NOT IN ('Insomnia', 'Sleep apnea')) AS No_Disorder_Count
FROM `term-project-421603.Sleep_Health.TransformedData`
GROUP BY Age_Group
"""

view4_id = 'term-project-421603.Sleep_Health.PhysicalActivity'
query4 =  """
SELECT `PhysicalActivityLevel`, COUNT(*) AS Count
FROM `term-project-421603.Sleep_Health.TransformedData`
GROUP BY `PhysicalActivityLevel`
"""

view5_id = 'term-project-421603.Sleep_Health.OccupationCount'
query5 = """
SELECT Occupation, COUNT(*) AS Count
FROM `term-project-421603.Sleep_Health.TransformedData`
GROUP BY Occupation
"""

# Creating views in BigQuery if they do not exist
views = [(view1_id, query1), (view2_id, query2), (view3_id, query3), (view4_id, query4), (view5_id, query5)]

for view_id, query in views:
    try:
        # Check if the view already exists
        client.get_table(view_id)
        print(f"View '{view_id}' already exists.")
    except NotFound:
        # Create the view if it doesn't exist
        view = bigquery.Table(view_id)
        view.view_query = query
        view = client.create_table(view)
        print(f"View '{view_id}' created successfully.")

# Fetching results into a dataframe
df1 = client.query(query1).to_dataframe()
df2 = client.query(query2).to_dataframe()
df3 = client.query(query3).to_dataframe()
df4 = client.query(query4).to_dataframe()
df5 = client.query(query5).to_dataframe()


# Visualization 1: Bar Chart of Average Sleep Duration by Gender
plt.figure(figsize=(10, 6))
plt.bar(df1['Gender'], df1['Avg_Sleep_Duration'])
plt.xlabel('Gender')
plt.ylabel('Average Sleep Duration')
plt.title('Average Sleep Duration by Gender')
plt.show()

# Visualization 2: Line Plot of Average Heart Rate by BMI Category
plt.figure(figsize=(10, 6))
plt.plot(df2['BMICategory'], df2['Avg_Heart_Rate'], marker='o')
plt.xlabel('BMI Category')
plt.ylabel('Average Heart Rate')
plt.title('Average Heart Rate by BMI Category')
plt.grid()
plt.show()

# Visualization 3: Pie Chart of Sleep Disorders by Age Group
plt.figure(figsize=(10, 8))
labels = df3['Age_Group']
insomnia_counts = df3['Insomnia_Count']
sleep_apnea_counts = df3['Sleep_Apnea_Count']
no_disorder_counts = df3['No_Disorder_Count']
plt.subplot(1, 2, 1)
plt.pie(insomnia_counts, labels=labels, autopct='%1.1f%%')
plt.title('Insomnia Distribution by Age Group')
plt.subplot(1, 2, 2)
plt.pie(sleep_apnea_counts, labels=labels, autopct='%1.1f%%')
plt.title('Sleep Apnea Distribution by Age Group')
plt.tight_layout()
plt.show()

# Visualization 4: Histogram of Physical Activity Level Distribution
plt.figure(figsize=(10, 6))
plt.hist(df4['PhysicalActivityLevel'])
plt.xlabel('Physical Activity Level')
plt.ylabel('Count')
plt.title('Physical Activity Level Distribution')
plt.grid(axis='y')
plt.show()

# Visualization 5: Box Plot of Quality of Sleep by Occupation
plt.figure(figsize=(12, 8))
plt.barh(df5['Occupation'], df5['Count'], color='skyblue')
plt.xlabel('Count')
plt.ylabel('Occupation')
plt.title('Occupation Distribution')
plt.gca().invert_yaxis()  # Invert y-axis to show the most common occupations at the top
plt.show()