/** @format */

$(document).ready(function () {
	function update() {
		var selectedDepartment = $("#department").val();
		var selectedYos = $("#yos").val();
		var selectedReason = $("#reason").val();
		var selectedOverallSatis = $("#overallSatis").val();
		var selectedRecomms = $("#recomms").val();
		var selectedWorkEnvs = $("#workEnvs").val();
		var selectedSalarySatis = $("#salarySatis").val();
		var selectedMngmtSatis = $("#mngmtSatis").val();
		var selectedGrowthOppurs = $("#growthOppurs").val();
		$.ajax({
			type: "POST",
			url: "/update_emp_exit",
			data: {
				department: selectedDepartment,
				yos: selectedYos,
				reason: selectedReason,
				overallSatis: selectedOverallSatis,
				recomms: selectedRecomms,
				workEnvs: selectedWorkEnvs,
				salarySatis: selectedSalarySatis,
				mngmtSatis: selectedMngmtSatis,
				growthOppurs: selectedGrowthOppurs,
			},
			success: function (response) {
				console.log("AJAX Response:", response);
				var columnNames = response.column_names;
				var exits = JSON.parse(response.json_emp_exit_data);

				// Clear existing headers and data
				$("#exit_data").empty();

				for (var i = 0; i < exits.length; i++) {
					// Create a new table row for each record
					var row = $("<tr>");
					for (var j = 0; j < exits[i].length; j++) {
						// Create a new table cell for each field
						var cell = $("<td>").text(exits[i][j]);
						row.append(cell);
					}
					var feedbackCell = $("<td>").html(
						'<a href="/feedback/' + exits[i][0] + '">Feedback</a>'
					);
					row.append(feedbackCell);
					$("#exit_data").append(row);
				}
			},
			error: function (error) {
				console.log("Error:", error);
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
