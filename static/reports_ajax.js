/** @format */

$(document).ready(function () {
	function update() {
		var selectedDepartment = $("#department").val();

		$.ajax({
			type: "POST",
			url: "/update_graphs",
			data: {
				department: selectedDepartment,
			},
			success: function () {
				document.getElementById("dept").innerHTML =
					"Department : " + selectedDepartment;
				document.getElementById("dateDay").innerHTML =
					"Date : " + formattedDate;
				updateGraph("overallSatisfactionGraph", "/satisfaction_graph");
				updateGraph("mngmtSatisfactionGraph", "/mngmt_satisfaction");
				updateGraph("salarySatisfactionGraph", "/salary_satisfaction");
				updateGraph("workEnvGraph", "/work_env");
				updateGraph("primaryReasonGraph", "/primary_reason_graph");
				updateGraph("growthOppurGraph", "/growth_oppur");
				updateGraph("companyRecommendGraph", "/company_Recommend");
				updateGraph("DistributionYOSGraph", "/distribution_yos");
				updateGraph("empLeftGraph", "/update_emp_left");
				updateGraph(
					"correlationSatisfactionGraph",
					"/correlation_satisfaction"
				);

				updateText("exits", "/emp_exit_table");
				updateText("avgYOS", "/avg_yos_table");
				updateText("overallSatisfactionAvg", "/avg_satisfaction_table");
				updateText("overallSatisfactionKPI", "/overallSatisfactionKPI");
				updateText("companyRecommendKPI", "/companyRecommendKPI");
				updateText("mngmtSatisfactionAvg", "/avg_mngmt_satisfaction_table");
				updateText("mngmtSatisfactionKPI", "/mngmtSatisfactionKPI");
				updateText("salarySatisfactionAvg", "/avg_salary_satisfaction_table");
				updateText("salarySatisfactionKPI", "/salarySatisfactionKPI");
				updateText("workEnvAvg", "/avg_work_env_table");
				updateText("workEnvKPI", "/workEnvKPI");
				updateTable(
					"factorCompanyRecommendTable",
					"/contri_to_recommend_table"
				);
				updateTable("predict1Table", "/predict1_table");
				updateTable("predict2Table", "/predict2_table");
			},
			error: function (error) {
				console.error("Error:", error);
			},
		});
	}

	function updateGraph(divId, url) {
		$.ajax({
			type: "POST",
			url: url,
			data: {
				department: $("#department").val(),
			},
			success: function (Graph) {
				// Update the graph container with the new image
				$("#" + divId).html(
					'<img src="data:image/png;base64,' +
						Graph[divId] +
						'" alt="Matplotlib Bar Graph">'
				);
			},
			error: function (error) {
				console.log(error);
			},
		});
	}

	function updateText(divId, url) {
		$.ajax({
			type: "POST",
			url: url,
			data: {
				department: $("#department").val(),
			},
			success: function (response) {
				// Update the text container with the new text
				$("#" + divId).text(response[divId]);
			},
			error: function (error) {
				console.log(error);
			},
		});
	}

	function updateTable(divId, url) {
		$.ajax({
			type: "POST",
			url: url,
			data: {
				department: $("#department").val(),
			},
			success: function (response) {
				// Update the text container with the new text
				$("#" + divId).html(response[divId]);
			},
			error: function (error) {
				console.log(error);
			},
		});
	}

	function printdiv(elem) {
		var header_str =
			"<html><head><title>" + document.title + "</title></head><body>";
		var footer_str = "</body></html>";
		var new_str = document.getElementById(elem).innerHTML;
		var old_str = document.body.innerHTML;
		document.body.innerHTML = header_str + new_str + footer_str;
		window.print();
		document.body.innerHTML = old_str;
		return false;
	}

	function formatDate(date) {
		const options = {
			weekday: "long",
			day: "numeric",
			month: "long",
			year: "numeric",
		};

		const formattedDate = new Intl.DateTimeFormat("en-GB", options).format(
			date
		);

		// Add suffix to the day
		const day = formattedDate.split(" ")[0];

		// Combine all parts
		const [, ...parts] = formattedDate.split(" ");
		return day + " " + parts.join(" ");
	}

	const date = new Date(); // You can replace this with your desired date
	const formattedDate = formatDate(date);
	console.log(formattedDate);

	$("#slicer-form").submit(function (e) {
		e.preventDefault();
		update();
	});

	update();

	setInterval(update, 60000);
});
