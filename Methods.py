from Connection import *


# Retrieve Users
def fetch_user():
    if conn.is_connected():
        cursor.execute("SELECT username, password FROM users")

        users = {}
        for row in cursor.fetchall():
            username = row[0]
            password = row[1]
            users[username] = {"username": username, "password": password}
        return users


# Fetch Exit Details
def select_employee_exit(
    selected_department,
    selected_yos,
    selected_reason,
    selected_overallSatis,
    selected_recomms,
    selected_workEnvs,
    selected_salarySatis,
    selected_mngmtSatis,
    selected_growthOppurs,
):
    filters = {
        "department": selected_department,
        "yr_of_service": selected_yos,
        "reason": selected_reason,
        "Overall_Satisfaction": selected_overallSatis,
        "recommend_company": selected_recomms,
        "Work_Environment_Rating": selected_workEnvs,
        "Salary_Satisfaction": selected_salarySatis,
        "Management_Satisfaction": selected_mngmtSatis,
        "growth_oppur": selected_growthOppurs,
    }
    if (
        selected_department == "All"
        and selected_yos == "All"
        and selected_reason == "All"
        and selected_overallSatis == "All"
        and selected_recomms == "All"
        and selected_workEnvs == "All"
        and selected_salarySatis == "All"
        and selected_mngmtSatis == "All"
        and selected_growthOppurs == "All"
    ):
        sql = f"SELECT * FROM emp_exit"
        # print(filters)

    else:
        if (
            selected_department != "All"
            or selected_yos != "All"
            or selected_reason != "All"
            or selected_overallSatis != "All"
            or selected_recomms != "All"
            or selected_workEnvs != "All"
            or selected_salarySatis != "All"
            or selected_mngmtSatis != "All"
            or selected_growthOppurs != "All"
        ):
            filtered_filters = {
                key: value for key, value in filters.items() if value != "All"
            }

            # print(filtered_filters)

            sql = "SELECT * FROM emp_exit WHERE " + " AND ".join(
                [f"{key}='{value}'" for key, value in filtered_filters.items()]
            )

            # print(sql)

    cursor.execute(sql)
    records = cursor.fetchall()
    return records


# Fetch Feedback Details
def select_feedback(e_id):
    sql = f"SELECT user, feedback FROM feedback where emp_id = {e_id}"
    cursor.execute(sql)
    records = cursor.fetchall()
    return records


# Add Feedback
def add_feedback(e_id, usr, feedbk):
    sql = f"INSERT INTO feedback VALUES (%s,%s,%s)"
    values = (e_id, usr, feedbk)
    cursor.execute(sql, values)
    conn.commit()
    return "Feedback Added......."
