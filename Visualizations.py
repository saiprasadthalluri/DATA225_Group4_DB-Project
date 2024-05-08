import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to MySQL server
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Data225DB",
    database="Sleep"
)

# Create a cursor object
cursor = connection.cursor()

# SQL query with joins to calculate average sleep duration by occupation
query = """
SELECT Occupation, AVG(SM.SleepDuration) AS AvgSleepDuration
FROM Person AS P
JOIN SleepMetrics AS SM ON P.PersonID = SM.SleepID
GROUP BY Occupation;
"""

# Execute the query and fetch the results
cursor.execute(query)
results = cursor.fetchall()

# Convert results to a DataFrame for easier manipulation
df = pd.DataFrame(results, columns=['Occupation', 'AvgSleepDuration'])

# Close the cursor and connection
cursor.close()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['Occupation'], df['AvgSleepDuration'], color='skyblue')
plt.xlabel('Occupation')
plt.ylabel('Average Sleep Duration')
plt.title('Average Sleep Duration by Occupation')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

query = """
SELECT P.Gender, SM.SleepDuration, M.StressLevel
FROM Person AS P
JOIN Sleepmetrics AS SM ON P.PersonID = SM.SleepID
JOIN Metrics AS M ON P.PersonID = M.MetricsID;
"""
df = pd.read_sql_query(query, connection)

# Create the lmplot using seaborn
sns.lmplot(x='SleepDuration', y='StressLevel', hue='Gender', data=df)
plt.title('Relationship between Sleep Duration and Stress Level (Segmented by Gender)')
plt.xlabel('Sleep Duration')
plt.ylabel('Stress Level')
plt.show()

query = """
SELECT Occupation, 
       SUM(CASE WHEN BMICategory = 'Normal' THEN 1 ELSE 0 END) AS Normal,
       SUM(CASE WHEN BMICategory = 'Overweight' THEN 1 ELSE 0 END) AS Overweight,
       SUM(CASE WHEN BMICategory = 'Obese' THEN 1 ELSE 0 END) AS Obese
FROM Person AS P
JOIN Metrics AS M ON P.PersonID = M.MetricsID
GROUP BY Occupation;
"""
df = pd.read_sql_query(query, connection)

# Create the stacked bar chart using matplotlib
df.set_index('Occupation').plot(kind='bar', stacked=True)
plt.title('Distribution of BMI Categories Across Occupations')
plt.xlabel('Occupation')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.legend(title='BMI Category')
plt.tight_layout()
plt.show()

query = """
SELECT 
    CASE 
        WHEN Age < 20 THEN 'Under 20'
        WHEN Age >= 20 AND Age < 30 THEN '20-29'
        WHEN Age >= 30 AND Age < 40 THEN '30-39'
        WHEN Age >= 40 AND Age < 50 THEN '40-49'
        ELSE '50+' 
    END AS AgeGroup,
    SUM(CASE WHEN SleepDisorder = 'Insomnia' THEN 1 ELSE 0 END) AS Insomnia,
    SUM(CASE WHEN SleepDisorder = 'Sleep Apnea' THEN 1 ELSE 0 END) AS SleepApnea,
    SUM(CASE WHEN SleepDisorder = 'None' THEN 1 ELSE 0 END) AS None
FROM Person AS P
JOIN Sleepmetrics AS SM ON P.PersonID = SM.SleepID
GROUP BY AgeGroup;
"""
df = pd.read_sql_query(query, connection)

# Create the stacked bar chart using matplotlib
df.set_index('AgeGroup').plot(kind='bar', stacked=True)
plt.title('Distribution of Sleep Disorders Across Age Groups')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.xticks(rotation=0)  # Rotate x-axis labels for better visibility
plt.legend(title='Sleep Disorder')
plt.tight_layout()
plt.show()

query = """
SELECT Gender, Age, QualityOfSleep
FROM Person AS P
JOIN Sleepmetrics AS SM ON P.PersonID = SM.SleepID;
"""
df = pd.read_sql_query(query, connection)

# Define age groups
def define_age_group(age):
    if 20 <= age <= 29:
        return '20-29'
    elif 30 <= age <= 39:
        return '30-39'
    elif 40 <= age <= 49:
        return '40-49'
    else:
        return '50+'

# Apply age group definition to the DataFrame
df['AgeGroup'] = df['Age'].apply(define_age_group)

# Create a violin plot using seaborn with split by age groups
plt.figure(figsize=(10, 6))
sns.violinplot(data=df, x='Gender', y='QualityOfSleep', hue='AgeGroup', inner='quartile')
plt.title('Distribution of Sleep Quality Across Gender and Age Groups')
plt.xlabel('Gender')
plt.ylabel('Quality of Sleep')
plt.legend(title='Age Group')
plt.tight_layout()
plt.show()


query = """
SELECT SM.SleepDuration, M.StressLevel, M.BMICategory
FROM Sleepmetrics AS SM
JOIN Metrics AS M ON SM.SleepID = M.MetricsID;

"""
df = pd.read_sql_query(query, connection)

# Create a scatter plot using seaborn with hue based on BMI category
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='SleepDuration', y='StressLevel', hue='BMICategory')
plt.title('Relationship between Sleep Duration and Stress Level (Segmented by BMI Category)')
plt.xlabel('Sleep Duration')
plt.ylabel('Stress Level')
plt.legend(title='BMI Category')
plt.tight_layout()
plt.show()