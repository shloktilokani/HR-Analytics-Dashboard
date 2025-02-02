import base64
from Analysis import *
from flask import *
import json
import os

app = Flask(__name__)


# Configure the Flask app to use Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False

users = fetch_user()
username = ""


# ---------------------------------------------------- Flask login ----------------------------------------------------


# home
@app.route("/")
def home():
    return redirect("/login")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    invalid_login = False  # Flag for invalid login attempt
    if session.get("logged_in"):
        return redirect("/graphs")
    if request.method == "POST":
        global username
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["logged_in"] = True
            return redirect("/graphs")
        else:
            invalid_login = True  # Set flag for invalid login attempt
    return render_template("login.html", invalid_login=invalid_login)


#                                               +++++ Protected Routes +++++
# Emp Exit Table View
@app.route("/emp_exit")
def emp_exit():
    if session.get("logged_in"):
        return render_template(
            "emp_exit.html",
            departments=filters("department"),
            yoss=filters("yr_of_service"),
            reasons=filters("reason"),
            overallSatis=filters("Overall_Satisfaction"),
            recomms=filters("recommend_company"),
            workEnvs=filters("Work_Environment_Rating"),
            salarySatis=filters("Salary_Satisfaction"),
            mngmtSatis=filters("Management_Satisfaction"),
            growthOppurs=filters("growth_oppur"),
        )
    else:
        return redirect("/")


@app.route("/update_emp_exit", methods=["POST"])
def update_emp_exit():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        selected_yos = request.form.get("yos")
        selected_reason = request.form.get("reason")
        selected_overallSatis = request.form.get("overallSatis")
        selected_recomms = request.form.get("recomms")
        selected_workEnvs = request.form.get("workEnvs")
        selected_salarySatis = request.form.get("salarySatis")
        selected_mngmtSatis = request.form.get("mngmtSatis")
        selected_growthOppurs = request.form.get("growthOppurs")

        emp_exit_data = select_employee_exit(
            selected_department,
            selected_yos,
            selected_reason,
            selected_overallSatis,
            selected_recomms,
            selected_workEnvs,
            selected_salarySatis,
            selected_mngmtSatis,
            selected_growthOppurs,
        )
        json_emp_exit_data = json.dumps(emp_exit_data)
        return jsonify({"json_emp_exit_data": json_emp_exit_data})
    else:
        return redirect("/")


# Graphs
@app.route("/graphs")
def graphs():
    if session.get("logged_in"):
        return render_template(
            "graphs.html",
            departments=filters("department"),
        )
    else:
        return redirect("/")


@app.route("/update_graphs", methods=["POST"])
def update_graphs():
    if session.get("logged_in"):
        selected_department = request.form.get("department")

        overallSatisfaction(selected_department)
        mngmtSatisfaction(selected_department)
        salarySatisfaction(selected_department)
        workEnv(selected_department)
        primaryReasons(selected_department)
        companyRecommend(selected_department)
        DistributionYOS(selected_department)
        empLeft()
        growthOppur(selected_department)
        correlationSatisfaction(selected_department)
        return jsonify({"status": "success"})
    else:
        return redirect("/")


# =========================================================================
@app.route("/growth_oppur", methods=["POST"])
def growth_oppur():
    if session.get("logged_in"):
        graph_path = "static/res/growthOppur.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"growthOppurGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/update_emp_left", methods=["POST"])
def update_emp_left():
    if session.get("logged_in"):
        graph_path = "static/res/empLeft.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"empLeftGraph": encoded_image})
    else:
        return redirect("/")


@app.route("/emp_exit_table", methods=["POST"])
def emp_exit_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify({"exits": empLeftTable(selected_department)})
    else:
        return redirect("/")


# =========================================================================
@app.route("/avg_yos_table", methods=["POST"])
def avg_yos_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify({"avgYOS": avgYosTable(selected_department)})
    else:
        return redirect("/")


@app.route("/distribution_yos", methods=["POST"])
def distribution_yos():
    if session.get("logged_in"):
        graph_path = "static/res/DistributionYOS.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"DistributionYOSGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/avg_satisfaction_table", methods=["POST"])
def avg_satisfaction_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"overallSatisfactionAvg": avgOverallRatingTable(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/satisfaction_graph", methods=["POST"])
def satisfaction_graph():
    if session.get("logged_in"):
        graph_path = "static/res/overallSatisfaction.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return jsonify({"overallSatisfactionGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/avg_mngmt_satisfaction_table", methods=["POST"])
def avg_mngmt_satisfaction_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"mngmtSatisfactionAvg": avgManagementRatingTable(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/mngmt_satisfaction", methods=["POST"])
def mngmt_satisfaction():
    if session.get("logged_in"):
        graph_path = "static/res/mngmtSatisfaction.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"mngmtSatisfactionGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/avg_salary_satisfaction_table", methods=["POST"])
def avg_salary_satisfaction_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"salarySatisfactionAvg": avgSalaryRatingTable(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/salary_satisfaction", methods=["POST"])
def salary_satisfaction():
    if session.get("logged_in"):
        graph_path = "static/res/salarySatisfaction.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"salarySatisfactionGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/avg_work_env_table", methods=["POST"])
def avg_work_env_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify({"workEnvAvg": avgWorkEnvRatingTable(selected_department)})
    else:
        return redirect("/")


@app.route("/work_env", methods=["POST"])
def work_env():
    if session.get("logged_in"):
        graph_path = "static/res/workEnv.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"workEnvGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/primary_reason_graph", methods=["POST"])
def primary_reason_graph():
    if session.get("logged_in"):
        graph_path = "static/res/primaryReasons.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"primaryReasonGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/contri_to_recommend_table", methods=["POST"])
def contri_to_recommend_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"factorCompanyRecommendTable": contriToRecommend(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/company_Recommend", methods=["POST"])
def company_Recommend():
    if session.get("logged_in"):
        graph_path = "static/res/companyRecommend.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"companyRecommendGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/correlation_satisfaction", methods=["POST"])
def correlation_satisfaction():
    if session.get("logged_in"):
        graph_path = "static/res/correlationSatisfaction.png"
        with open(graph_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"correlationSatisfactionGraph": encoded_image})
    else:
        return redirect("/")


# =========================================================================
@app.route("/predict1_table", methods=["POST"])
def predict1_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify({"predict1Table": predict1(selected_department)})
    else:
        return redirect("/")


@app.route("/predict2_table", methods=["POST"])
def predict2_table():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify({"predict2Table": predict2(selected_department)})
    else:
        return redirect("/")


# =========================================================================
@app.route("/overallSatisfactionKPI", methods=["POST"])
def overallSatisfactionKPI():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"overallSatisfactionKPI": overAllSatisfactionRate(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/mngmtSatisfactionKPI", methods=["POST"])
def mngmtSatisfactionKPI():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"mngmtSatisfactionKPI": ManagementSatisfactionRate(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/salarySatisfactionKPI", methods=["POST"])
def salarySatisfactionKPI():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"salarySatisfactionKPI": SalarySatisfactionRate(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/workEnvKPI", methods=["POST"])
def workEnvKPI():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"workEnvKPI": workEnvironmentSatisfactionRate(selected_department)}
        )
    else:
        return redirect("/")


@app.route("/companyRecommendKPI", methods=["POST"])
def companyRecommendKPI():
    if session.get("logged_in"):
        selected_department = request.form.get("department")
        return jsonify(
            {"companyRecommendKPI": employeeRecommendationRate(selected_department)}
        )
    else:
        return redirect("/")


# =========================================================================


# Reports
@app.route("/reports")
def reports():
    if session.get("logged_in"):
        return render_template("reports.html", departments=filters("department"))
    else:
        return redirect("/")


# Feedback
@app.route("/feedback/<int:record_id>", methods=["GET", "POST"])
def feedback(record_id):
    if session.get("logged_in"):
        emp_exit_data = select_employee_exit(
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
        if 0 < record_id <= len(emp_exit_data):
            # Check if record_id is valid
            first_column_value = emp_exit_data[record_id - 1][0]
            print(first_column_value)
            feedback_data = select_feedback(e_id=first_column_value)
            if request.method == "POST":
                e_id = first_column_value
                usr = username
                feedbk = request.form["feed"]
                add_feedback(e_id=e_id, usr=usr, feedbk=feedbk)
                return redirect(f"/feedback/{record_id}")
            return render_template(
                "feedback.html",
                first_column_value=first_column_value,
                feedback_data=feedback_data,
            )
        else:
            return "Invalid record ID"
    else:
        return redirect("/")


# Logout route
@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
