import mysql.connector
import dask.dataframe as dd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.impute import SimpleImputer
import numpy as np
from matplotlib import pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin,Root",
    database="dashboard_db",
)
if conn.is_connected():
    print("Connected to MySQL database")

# Cursor Object For Interaction
cursor = conn.cursor()

query = "SELECT * FROM emp_exit"
cursor.execute(query)
emp_exit = cursor.fetchall()
columns = [i[0] for i in cursor.description]
df = dd.from_pandas(
    pd.DataFrame(emp_exit, columns=columns), npartitions=4
)  # Convert to Dask DataFrame
pandas_df = df.compute()

# Assuming you have X_train, X_test, y_train, and y_test defined

# Replace 'None' with NaN
pandas_df.replace("None", np.nan, inplace=True)

X = pandas_df[["Work_Environment_Rating", "growth_oppur"]]
y = pandas_df[["Overall_Satisfaction"]]

# Convert columns to numeric
X = X.apply(pd.to_numeric, errors="coerce")
y = y.apply(pd.to_numeric, errors="coerce")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Impute NaN values for both X_train and X_test
imputer = SimpleImputer(strategy="mean")
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)
y_train = imputer.fit_transform(y_train)

model = LinearRegression()
model.fit(X_train, y_train)

# Check for NaN values in X_test before making predictions
if np.isnan(X_test).any():
    print("Warning: X_test contains NaN values. Please check your data.")

# Make predictions on the test set
y_pred = model.predict(X_test)

# # Evaluate the model
# print("Mean Absolute Error:", metrics.mean_absolute_error(y_test, y_pred))
# print("Mean Squared Error:", metrics.mean_squared_error(y_test, y_pred))
# print(
#     "Root Mean Squared Error:",
#     metrics.mean_squared_error(y_test, y_pred, squared=False),
# )

X_test_df = pd.DataFrame(X_test, columns=["Work_Environment_Rating", "growth_oppur"])

# Visualize the predictions
plt.scatter(X_test_df["Work_Environment_Rating"], y_test.values, color="black")
plt.scatter(X_test_df["Work_Environment_Rating"], y_pred, color="blue", linewidth=3)
plt.xlabel("Work Environment Rating")
plt.ylabel("Overall Satisfaction")
plt.show()
