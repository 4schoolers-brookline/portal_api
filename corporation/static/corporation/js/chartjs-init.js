 (function($) {
   "use strict"


	/* function draw() {

	} */

 var dzSparkLine = function(){
	let draw = Chart.controllers.line.__super__.draw; //draw shadow

	var screenWidth = $(window).width();

	var weekLessonsChart = function(){
		if(jQuery('#weekLessonsChart').length > 0 ){
			var lessons = $.parseJSON(
				$.ajax({
					url: '/activity/api/corporation_lessons_week',
					dataType: 'json',
					async:false
				}).responseText
			);
			const barChart_1 = document.getElementById("weekLessonsChart").getContext('2d');

			barChart_1.height = 40;

			new Chart(barChart_1, {
				type: 'bar',
				data: {
					defaultFontFamily: 'Poppins',
					labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
					datasets: [
						{
							label: "Hours spent",
							data: lessons,
							borderColor: 'rgba(41, 51, 242, 1)',
							borderWidth: "0",
							backgroundColor: 'rgba(41, 51, 242, 1)'
						}
					]
				},
				options: {
					legend: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true
							}
						}],
						xAxes: [{
							// Change here
							barPercentage: 0.5
						}]
					}
				}
			});
		}
	}

	var yearLessonsChart = function(){
		if(jQuery('#yearLessonsChart').length > 0 ){
			var lessons = $.parseJSON(
				$.ajax({
					url: '/activity/api/corporation_lessons_year',
					dataType: 'json',
					async:false
				}).responseText
			);

		//gradient bar chart
			const barChart_2 = document.getElementById("yearLessonsChart").getContext('2d');
			//generate gradient
			const barChart_2gradientStroke = barChart_2.createLinearGradient(0, 0, 0, 250);
			barChart_2gradientStroke.addColorStop(0, "rgba(41, 51, 242, 1)");
			barChart_2gradientStroke.addColorStop(1, "rgba(41, 51, 242, 0.5)");

			barChart_2.height = 100;

			new Chart(barChart_2, {
				type: 'bar',
				data: {
					defaultFontFamily: 'Poppins',
					labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
					datasets: [
						{
							label: "Time spent this month",
							data: lessons,
							borderColor: barChart_2gradientStroke,
							borderWidth: "0",
							backgroundColor: barChart_2gradientStroke,
							hoverBackgroundColor: barChart_2gradientStroke
						}
					]
				},
				options: {
					legend: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true
							}
						}],
						xAxes: [{
							// Change here
							barPercentage: 0.5
						}]
					}
				}
			});
		}
	}
	var monthLessonsChart = function(){
		if(jQuery('#monthLessonsChart').length > 0 ){

			var lessons = $.parseJSON(
				$.ajax({
					url: '/activity/api/corporation_lessons_month',
					dataType: 'json',
					async:false
				}).responseText
			);
		//gradient bar chart
			const barChart_3 = document.getElementById("monthLessonsChart").getContext('2d');
			//generate gradient
			const barChart_2gradientStroke = barChart_3.createLinearGradient(0, 0, 0, 250);
			barChart_2gradientStroke.addColorStop(0, "rgba(41, 51, 242, 1)");
			barChart_2gradientStroke.addColorStop(1, "rgba(41, 51, 242, 0.5)");

			barChart_3.height = 100;

			new Chart(barChart_3, {
				type: 'bar',
				data: {
					defaultFontFamily: 'Poppins',
					labels: lessons.total,
					datasets: [
						{
							label: "Time spent this month",
							data: lessons.days,
							borderColor: barChart_2gradientStroke,
							borderWidth: "0",
							backgroundColor: barChart_2gradientStroke,
							hoverBackgroundColor: barChart_2gradientStroke
						}
					]
				},
				options: {
					legend: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true
							}
						}],
						xAxes: [{
							barPercentage: 0.5
						}]
					}
				}
			});
		}
	}



	var studentsChart = function(){
		//pie chart
		if(jQuery('#students_chart').length > 0 ){
			var lessons = $.parseJSON(
				$.ajax({
					url: '/activity/api/corporation_students_lessons',
					dataType: 'json',
					async:false
				}).responseText
			);

			//pie chart
			const pie_chart = document.getElementById("students_chart").getContext('2d');
			// pie_chart.height = 100;
			new Chart(pie_chart, {
				type: 'pie',
				data: {
					defaultFontFamily: 'Poppins',
					datasets: [{
						data: lessons.lessons,
						borderWidth: 0,
						backgroundColor: [
							"rgba(41, 51, 242, .9)",
							"rgba(41, 51, 242, .7)",
							"rgba(41, 51, 242, .5)",
							"rgba(0,0,0,0.07)"
						],
						hoverBackgroundColor: [
							"rgba(41, 51, 242, .9)",
							"rgba(41, 51, 242, .7)",
							"rgba(41, 51, 242, .5)",
							"rgba(0,0,0,0.07)"
						]

					}],
					labels: lessons.students
				},
				options: {
					responsive: true,
					legend: false,
					maintainAspectRatio: false
				}
			});
		}
	}
	var subjectsLessonChart = function(){
		//pie chart
		if(jQuery('#subjectsLessonChart').length > 0 ){
			var lessons = $.parseJSON(
				$.ajax({
					url: '/activity/api/corporation_subjects_lessons',
					dataType: 'json',
					async:false
				}).responseText
			);

			//pie chart
			const pie_chart = document.getElementById("subjectsLessonChart").getContext('2d');
			// pie_chart.height = 100;
			new Chart(pie_chart, {
				type: 'pie',
				data: {
					defaultFontFamily: 'Poppins',
					datasets: [{
						data: lessons.lessons,
						borderWidth: 0,
						backgroundColor: [
							"rgba(41, 51, 242, .9)",
							"rgba(41, 51, 242, .7)",
							"rgba(41, 51, 242, .5)",
							"rgba(0,0,0,0.07)"
						],
						hoverBackgroundColor: [
							"rgba(41, 51, 242, .9)",
							"rgba(41, 51, 242, .7)",
							"rgba(41, 51, 242, .5)",
							"rgba(0,0,0,0.07)"
						]

					}],
					labels: lessons.subjects
				},
				options: {
					responsive: true,
					legend: false,
					maintainAspectRatio: false
				}
			});
		}
	}

	/* Function ============ */
	return {
		init:function(){
		},


		load:function(){
			weekLessonsChart();
			yearLessonsChart();
			monthLessonsChart();

			studentsChart();
			subjectsLessonChart();
		},

		resize:function(){
			// barChart1();
			// barChart2();
			// barChart3();
			// lineChart1();
			// lineChart2();
			// lineChart3();
			// lineChart03();
			// areaChart1();
			// areaChart2();
			// areaChart3();
			// radarChart();
			// pieChart();
			// doughnutChart();
			// polarChart();
		}
	}

}();



jQuery(window).on('load',function(){
	dzSparkLine.load();
});

jQuery(window).on('resize',function(){
	//dzSparkLine.resize();
	setTimeout(function(){ dzSparkLine.resize(); }, 1000);
});

})(jQuery);
