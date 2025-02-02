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

	$("#slicer-form").submit(function (e) {
		e.preventDefault();
		update();
	});

	update();

	setInterval(update, 60000);
});
