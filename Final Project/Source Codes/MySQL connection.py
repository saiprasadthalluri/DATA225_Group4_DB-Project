import mysql.connector
import pandas as pd

# Database Credentials
host = "127.0.0.1"
user = "root"
password = "Data225DB"

# Connect to MySQL server
try:
    connection = mysql.connector.connect(host=host, user=user, password=password)
    print("Connected to MySQL server successfully!")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL server: {err}")
    exit()

cursor = connection.cursor()

# Database name
database_name = "Sleep"

# Checking if database exists
try:
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    database_exists = cursor.fetchone() is not None
except mysql.connector.Error as err:
    print(f"Error checking for database: {err}")
    database_exists = False

if not database_exists:
    try:
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created successfully!")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        exit()

cursor.execute(f"USE {database_name}")

# Creating Person table
create_person_query = """
    CREATE TABLE IF NOT EXISTS Person (
        PersonID INT AUTO_INCREMENT PRIMARY KEY,
        Gender VARCHAR(255),
        Age INT,
        Occupation VARCHAR(255)
    )
"""

# Creating Sleep Metrics table
create_sleep_metrics_query = """
CREATE TABLE IF NOT EXISTS SleepMetrics (
    SleepID INT AUTO_INCREMENT PRIMARY KEY,
    SleepDuration FLOAT,
    QualityOfSleep INT,
    SleepDisorder VARCHAR(255)
)
"""

# Creating Physical Activity table
create_physical_activity_query = """
CREATE TABLE IF NOT EXISTS PhysicalActivity (
    PhysicalActivityID INT AUTO_INCREMENT PRIMARY KEY,
    PhysicalActivityLevel INT,
    DailySteps INT
)
"""

# Creating Metrics table
create_metrics_query = """
CREATE TABLE IF NOT EXISTS Metrics (
    MetricsID INT AUTO_INCREMENT PRIMARY KEY,
    StressLevel INT,
    BMICategory VARCHAR(255),
    BloodPressure VARCHAR(255),
    HeartRate INT
)
"""

# Execute the table creation queries
try:
    cursor.execute(create_person_query)
    cursor.execute(create_sleep_metrics_query)
    cursor.execute(create_physical_activity_query)
    cursor.execute(create_metrics_query)
    print("Tables created successfully!")
except mysql.connector.Error as err:
    print(f"Error creating tables: {err}")

# Creating Fact table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fact (
        FactID INT AUTO_INCREMENT PRIMARY KEY,
        PersonID INT,
        SleepID INT,
        PhysicalActivityID INT,
        MetricsID INT,
        FOREIGN KEY (PersonID) REFERENCES Person(PersonID),
        FOREIGN KEY (SleepID) REFERENCES SleepMetrics(SleepID),
        FOREIGN KEY (PhysicalActivityID) REFERENCES PhysicalActivity(PhysicalActivityID),
        FOREIGN KEY (MetricsID) REFERENCES Metrics(MetricsID)
    )
""")
print("Fact table created successfully!")

# Reading data from CSV file into DataFrame
csv_file_path = r"C:\Users\manjo\OneDrive\Documents\Homework\DATA 225\Datasets\Sleep_health_and_lifestyle_dataset.csv"
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: CSV file '{csv_file_path}' not found!")
    exit()

# Inserting data into Person table
person_data = df[["Person ID", "Gender", "Age", "Occupation"]].values.tolist()
cursor.executemany("INSERT IGNORE INTO Person (PersonID, Gender, Age, Occupation) VALUES (%s, %s, %s, %s)", person_data)
print("Data inserted into Person table successfully!")

# Inserting data into Sleep table
insert_query = """
    INSERT IGNORE INTO SleepMetrics (SleepDuration, QualityOfSleep, SleepDisorder)
    VALUES (%s, %s, %s)
"""

sleep_data = df[["Sleep Duration", "Quality of Sleep", "Sleep Disorder"]].values.tolist()

try:
    cursor.executemany(insert_query, sleep_data)
    print("Data inserted into Sleep table successfully!")
except mysql.connector.Error as err:
    print(f"Error inserting data into Sleep table: {err}")
    exit()

# Inserting data into PhysicalActivity table
physical_activity_data = df[["Physical Activity Level", "Daily Steps"]].values.tolist()
cursor.executemany("INSERT IGNORE INTO PhysicalActivity (PhysicalActivityLevel, DailySteps) VALUES (%s, %s)", physical_activity_data)
print("Data inserted into PhysicalActivity table successfully!")

# Inserting data into Metrics table
metrics_data = df[["Stress Level", "BMI Category", "Blood Pressure", "Heart Rate"]].values.tolist()
cursor.executemany("INSERT IGNORE INTO Metrics (StressLevel, BMICategory, BloodPressure, HeartRate) VALUES (%s, %s, %s, %s)", metrics_data)
print("Data inserted into Metrics table successfully!")

# Inserting data into Fact table
insert_query = """
INSERT IGNORE INTO Fact (PersonID, SleepID, PhysicalActivityID, MetricsID)
SELECT P.PersonID, SM.SleepID, PA.PhysicalActivityID, M.MetricsID
FROM Person AS P
JOIN SleepMetrics AS SM ON P.PersonID = SM.SleepID
JOIN PhysicalActivity AS PA ON P.PersonID = PA.PhysicalActivityID
JOIN Metrics AS M ON P.PersonID = M.MetricsID
"""

# Executing the fact table insert query
try:
    cursor.execute(insert_query)
    connection.commit()
    print("Data inserted into Fact table successfully!")
except mysql.connector.Error as err:
    print(f"Error inserting data into Fact table: {err}")
    connection.rollback()


# Updating the BMI Category values
update_query = """
UPDATE Metrics
SET BMICategory = 'Normal'
WHERE BMICategory IN ('Normal', 'Normal Weight')
"""
cursor.execute(update_query)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("All tables (dimension and fact) created successfully!")
