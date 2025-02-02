from Methods import *
import dask.dataframe as dd
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import textwrap
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
import matplotlib
import statistics as stats

matplotlib.use("Agg")


#                       ++++++++++++++++++++ Dataset for analysis ++++++++++++++++++++

# EMP_EXIT_DETAILS
dataSet = select_employee_exit(
    "All",
    "All",
    "All",
    "All",
    "All",
    "All",
    "All",
    "All",
    "All",
)

columns = [i[0] for i in cursor.description]
df = dd.from_pandas(pd.DataFrame(dataSet, columns=columns), npartitions=4)
pandas_df = df.compute()


# ------------------------------------ Pre-Processing -------------------------------------
growth_oppur_mapping = {
    "None": 0,
    "Limited": 1,
    "Adequate": 2,
    "Excellent": 3,
}
pandas_df["growth_oppur_num"] = pandas_df["growth_oppur"].map(growth_oppur_mapping)

recommend_mapping = {
    "Yes": 1,
    "No": 0,
}
pandas_df["recommend_num"] = pandas_df["recommend_company"].map(recommend_mapping)


# ---------------------------------------- Filters ----------------------------------------


def filters(param):
    fltr = sorted(pandas_df[param].unique().tolist())
    fltr.insert(0, "All")
    return fltr


def satisfactionList():
    satisfactionFields = [
        "Overall_Satisfaction",
        "Work_Environment_Rating",
        "Salary_Satisfaction",
        "Management_Satisfaction",
    ]
    return satisfactionFields


# ---------------------------------------- Graphs ----------------------------------------


# Pie-Chart Values
def pieValues(pct, allvalues):
    allvalues_float = [float(value) for value in allvalues]
    absolute = round(pct / 100 * np.sum(allvalues_float))
    return "{:}".format(absolute)


def matrixParamDepartment(param):
    result = {}
    for department, group in pandas_df.groupby("department"):
        counts = group[param].value_counts().sort_index()
        result[department] = counts
    result_df = pd.DataFrame(result)
    table_html = result_df.to_html(index=False)
    return table_html


# Pie Plots method
def piePlots(
    count,
    name,
    title,
    selected_department,
):
    if selected_department == "All":
        data = pandas_df
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        data = filtered_df

    plt.figure(figsize=(8, 5))
    pies = data[count].value_counts()

    data_values = []
    for data in pies.tolist():
        data_values.append(data)

    # Plot a pie chart
    plt.pie(
        pies,
        labels=pies.index,
        autopct=lambda pct: (pieValues(pct, data_values)),
        startangle=90,
    )

    plt.title(f"Graph of {title.capitalize()}")
    plt.savefig(f"static/res/{name}.png")
    plt.close()


# Bar Plots Method
def barPlots(
    count,
    name,
    title,
    selected_department,
):
    if selected_department == "All":
        data = pandas_df
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        data = filtered_df

    plt.figure(figsize=(9, 6))

    # Use bar plot to create a bar graph
    bars = sns.countplot(
        data=data,
        x=count,
        width=0.5,
    )

    # Display count values on top of the bars
    for bar in bars.patches:
        bars.annotate(
            format(bar.get_height(), ".0f"),
            (bar.get_x() + bar.get_width() / 2.0, bar.get_height()),
            ha="center",
            va="bottom",
            xytext=(0, 2),
            textcoords="offset points",
        )

    plt.title(f"Graph of {title}")
    plt.savefig(f"static/res/{name}.png")
    plt.close()


# ======================================================================================================================
#                                 ************ Descriptive Analysis ************
# Q1:What is the average satisfaction rating among exiting employees?
def AvgRatingTables(selected_department, param):
    if selected_department == "All":
        value = stats.mean(pandas_df[param])
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        value = stats.mean(filtered_df[param])
    return "{:.2f}".format(value)


def avgOverallRatingTable(selected_department):
    return AvgRatingTables(
        selected_department=selected_department, param="Overall_Satisfaction"
    )


def avgManagementRatingTable(selected_department):
    return AvgRatingTables(
        selected_department=selected_department, param="Management_Satisfaction"
    )


def avgSalaryRatingTable(selected_department):
    return AvgRatingTables(
        selected_department=selected_department, param="Salary_Satisfaction"
    )


def avgWorkEnvRatingTable(selected_department):
    return AvgRatingTables(
        selected_department=selected_department, param="Work_Environment_Rating"
    )


# Bar Graph - Overall Satisfaction Ratings
def overallSatisfaction(
    selected_department,
):
    barPlots(
        count="Overall_Satisfaction",
        name="overallSatisfaction",
        title="Overall Satisfaction Rating",
        selected_department=selected_department,
    )


# Bar Graph - Management Satisfaction Ratings
def mngmtSatisfaction(
    selected_department,
):
    barPlots(
        count="Management_Satisfaction",
        name="mngmtSatisfaction",
        title="Management Satisfaction Rating",
        selected_department=selected_department,
    )


# Bar Graph - Salary Satisfaction Ratings
def salarySatisfaction(
    selected_department,
):
    barPlots(
        count="Salary_Satisfaction",
        name="salarySatisfaction",
        title="Salary Satisfaction Rating",
        selected_department=selected_department,
    )


# Bar Graph - Work Environment Satisfaction Ratings
def workEnv(
    selected_department,
):
    barPlots(
        count="Work_Environment_Rating",
        name="workEnv",
        title="Work Environment Rating",
        selected_department=selected_department,
    )


# ..................................................................
# Q2:What are the primary reasons employees are leaving?


# Bar Graph - Employee Left:Reason Distribution
def primaryReasons(
    selected_department,
):
    barPlots(
        count="reason",
        name="primaryReasons",
        title="Primary Reasons for exit",
        selected_department=selected_department,
    )


# Bar Graph - Growth Oppur Ratings
def growthOppur(
    selected_department,
):
    barPlots(
        count="growth_oppur",
        name="growthOppur",
        title="Growth Oppurtunity Rating",
        selected_department=selected_department,
    )


# ..................................................................
# Q3:What are the average years of service for employees leaving the company?
def avgYosTable(selected_department):
    return AvgRatingTables(
        selected_department=selected_department, param="yr_of_service"
    )


# Bar Graph - Distribution of YOS?
def DistributionYOS(
    selected_department,
):
    barPlots(
        count="yr_of_service",
        name="DistributionYOS",
        title="Distribution of Years of Service",
        selected_department=selected_department,
    )


# ..................................................................
# Q4:How many employees have left from each department?
def empLeftTable(selected_department):
    if selected_department == "All":
        value = len(pandas_df["emp_id"])
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        value = len(filtered_df["emp_id"])
    return str(value)


# Bar Graph - Employee Left:Department Distribution
def empLeft():
    barPlots(
        count="department",
        name="empLeft",
        title="Employees Left By Department",
        selected_department="All",
    )


# Pie Chart - Employee Left:Recommendation Distribution
def companyRecommend(
    selected_department,
):
    piePlots(
        count="recommend_company",
        name="companyRecommend",
        title="Employees who will recommend company",
        selected_department=selected_department,
    )


# ----------------------------------------------------------------------------------------------------------------------
#                                 ************ Correlational Analysis ************
def correlationSatisfaction(selected_department):
    if selected_department == "All":
        correlation_matrix = pandas_df[
            [
                "Overall_Satisfaction",
                "Work_Environment_Rating",
                "Salary_Satisfaction",
                "Management_Satisfaction",
                "growth_oppur_num",
                "recommend_num",
            ]
        ].corr()
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        correlation_matrix = filtered_df[
            [
                "Overall_Satisfaction",
                "Work_Environment_Rating",
                "Salary_Satisfaction",
                "Management_Satisfaction",
                "growth_oppur_num",
                "recommend_num",
            ]
        ].corr()

    # Create a figure and axis
    plt.figure(figsize=(10, 8))

    # Wrap x-axis tick labels
    wrapped_labels = [
        textwrap.fill(label, width=10) for label in correlation_matrix.columns
    ]
    sns.heatmap(
        correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
    )

    bar_positions = [pos + 0.5 for pos in range(len(correlation_matrix.columns))]

    # Set wrapped x-axis tick labels
    plt.xticks(
        ticks=bar_positions,
        labels=wrapped_labels,
        rotation=0,
    )

    plt.yticks(
        ticks=bar_positions,
        labels=wrapped_labels,
        rotation=0,
    )

    # Set other properties as needed
    plt.title("Correlation Matrix")
    plt.savefig("static/res/correlationSatisfaction.png")
    plt.close()


# ----------------------------------------------------------------------------------------------------------------------
#                                 ************* Predictive Analysis *************
# y=m1x1+m2x2+b


# Can we predict an employee's Overall Satisfaction based on their Work Environment Rating and Opportunities for Growth?
def predict1(selected_department):
    if selected_department == "All":
        x = pandas_df[["Work_Environment_Rating", "growth_oppur_num"]]
        y = pandas_df["Overall_Satisfaction"]
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        x = filtered_df[["Work_Environment_Rating", "growth_oppur_num"]]
        y = filtered_df["Overall_Satisfaction"]

    model = linear_model.LinearRegression()
    model.fit(x, y)
    x1_lst = sorted(pandas_df.Work_Environment_Rating.unique().tolist())
    x2_lst = sorted(pandas_df.growth_oppur_num.unique().tolist())
    prediction = pd.DataFrame()
    workEnvRating = []
    growthOppurt = []
    overallSatisfactionRating = []
    for i in x1_lst:
        for j in x2_lst:
            y = model.predict(
                pd.DataFrame({"Work_Environment_Rating": [i], "growth_oppur_num": [j]})
            )
            if y >= 3:
                key = list(
                    filter(
                        lambda val: growth_oppur_mapping[val] == j, growth_oppur_mapping
                    )
                )[0]
                workEnvRating.append(i)
                growthOppurt.append(key)
                overallSatisfactionRating.append(y[0])
    prediction["Work_Environment_Rating"] = workEnvRating
    prediction["growth_oppur"] = growthOppurt
    prediction["Overall_Satisfaction"] = overallSatisfactionRating
    prediction = prediction.rename(
        columns={
            "Work_Environment_Rating": "Work Environment Rating",
            "growth_oppur": "Growth Opportunity",
            "Overall_Satisfaction": "Overall Satisfaction",
        }
    )
    table_html = prediction.to_html(index=False)
    return table_html


# Is it possible to predict if an employee would recommend the company using their Salary Satisfaction and Management Satisfaction scores?
def predict2(selected_department):
    if selected_department == "All":
        x = pandas_df[["Salary_Satisfaction", "Management_Satisfaction"]]
        y = pandas_df["recommend_company"]
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        x = filtered_df[["Salary_Satisfaction", "Management_Satisfaction"]]
        y = filtered_df["recommend_company"]

    model = linear_model.LogisticRegression()
    model.fit(x, y)
    x1_lst = sorted(pandas_df.Salary_Satisfaction.unique().tolist())
    x2_lst = sorted(pandas_df.Management_Satisfaction.unique().tolist())
    prediction = pd.DataFrame()
    salarySatisfactionRating = []
    managementSatisfactionRating = []
    recommendCompany = []
    for i in x1_lst:
        for j in x2_lst:
            y = model.predict(
                pd.DataFrame(
                    {"Salary_Satisfaction": [i], "Management_Satisfaction": [j]}
                )
            )
            if y == "Yes":
                salarySatisfactionRating.append(i)
                managementSatisfactionRating.append(j)
                recommendCompany.append(y[0])
    prediction["Salary_Satisfaction"] = salarySatisfactionRating
    prediction["Management_Satisfaction"] = managementSatisfactionRating
    prediction["recommend_company"] = recommendCompany
    prediction = prediction.rename(
        columns={
            "Salary_Satisfaction": "Salary Satisfaction",
            "Management_Satisfaction": "Management Satisfaction",
            "recommend_company": "Recommend Company?",
        }
    )
    table_html = prediction.to_html(index=False)
    return table_html


# ----------------------------------------------------------------------------------------------------------------------
#                                 ************* KPIs *************
# Are there specific factors that strongly influence an employee's likelihood to recommend the company?
def contriToRecommend(selected_department):
    if selected_department == "All":
        X = pandas_df[
            [
                "Overall_Satisfaction",
                "Salary_Satisfaction",
                "Management_Satisfaction",
                "Work_Environment_Rating",
                "growth_oppur_num",
            ]
        ]
        y = (pandas_df["recommend_company"] == "Yes").astype(int)
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        X = filtered_df[
            [
                "Overall_Satisfaction",
                "Salary_Satisfaction",
                "Management_Satisfaction",
                "Work_Environment_Rating",
                "growth_oppur_num",
            ]
        ]
        y = (filtered_df["recommend_company"] == "Yes").astype(int)
    model = RandomForestClassifier(random_state=50)
    model.fit(X, y)
    feature_importances = pd.Series(
        model.feature_importances_ * 100, index=X.columns
    ).sort_values(ascending=False)
    contri_df = pd.DataFrame(feature_importances)
    new_labels = [
        "Work Environment Rating",
        "Growth Opportunity",
        "Overall Satisfaction",
        "Salary Satisfaction",
        "Management Satisfaction",
    ]
    contri_df.index = new_labels
    contri_df[0] = contri_df[0].astype(str) + "%"
    table_html = contri_df.to_html(header=False)
    return table_html


def SatisfactionRateCalc(selected_department, param):
    if selected_department == "All":
        highCounts = pandas_df[param].isin([3, 4, 5]).value_counts().tolist()[0]
        total = len(pandas_df.emp_id)
    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        highCounts = filtered_df[param].isin([3, 4, 5]).value_counts().tolist()[0]
        total = len(filtered_df.emp_id)
    val = (highCounts / total) * 100
    return "{:.2f}".format(val) + "%"


# Overall Satisfaction Rate
def overAllSatisfactionRate(selected_department):
    return SatisfactionRateCalc(
        selected_department=selected_department, param="Overall_Satisfaction"
    )


# Work Environment Satisfaction Rate
def workEnvironmentSatisfactionRate(selected_department):
    return SatisfactionRateCalc(
        selected_department=selected_department, param="Work_Environment_Rating"
    )


# Salary Satisfaction Rate
def SalarySatisfactionRate(selected_department):
    return SatisfactionRateCalc(
        selected_department=selected_department, param="Salary_Satisfaction"
    )


# Management Satisfaction Rate
def ManagementSatisfactionRate(selected_department):
    return SatisfactionRateCalc(
        selected_department=selected_department, param="Management_Satisfaction"
    )


# Employee Recommendation Rate
def employeeRecommendationRate(selected_department):
    if selected_department == "All":
        highCounts = pandas_df["recommend_company"].eq("Yes").sum()
        total = len(pandas_df.emp_id)

    else:
        filtered_df = pandas_df[pandas_df["department"] == selected_department]
        highCounts = filtered_df["recommend_company"].eq("Yes").sum()
        total = len(filtered_df.emp_id)
    val = (highCounts / total) * 100
    return "{:.2f}".format(val) + "%"
