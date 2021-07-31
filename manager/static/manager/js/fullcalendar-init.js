(function($) {
    "use strict"

document.addEventListener('DOMContentLoaded', function() {

		/* initialize the external events
		-----------------------------------------------------------------*/
	var containerEl = document.getElementById('external-events');
	new FullCalendar.Draggable(containerEl, {
	  itemSelector: '.external-event',
	  eventData: function(eventEl) {
		return {
		  title: eventEl.innerText.trim()
		}
	  }

	});

	//// the individual way to do it
	// var containerEl = document.getElementById('external-events-list');
	// var eventEls = Array.prototype.slice.call(
	//   containerEl.querySelectorAll('.fc-event')
	// );
	// eventEls.forEach(function(eventEl) {
	//   new FullCalendar.Draggable(eventEl, {
	//     eventData: {
	//       title: eventEl.innerText.trim(),
	//     }
	//   });
	// });

	/* initialize the calendar
	-----------------------------------------------------------------*/



	var lessons = $.parseJSON(
		$.ajax({
			url: '/activity/api/manager_lessons',
			dataType: 'json',
			async:false
		}).responseText
	);

	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = today.getFullYear();





	var calendarEl = document.getElementById('calendar');
	var calendar = new FullCalendar.Calendar(calendarEl, {
	  headerToolbar: {
		left: 'prev,next today',
		center: 'title',
		right: 'dayGridMonth,timeGridWeek,timeGridDay'
	  },

	  selectable: true,
	  selectMirror: true,
	  select: function(arg) {
		var title = prompt('Event Title:');
		if (title) {
		  calendar.addEvent({
			title: title,
			start: arg.start,
			end: arg.end,
			allDay: arg.allDay
		  })
		}
		calendar.unselect()
	  },

	  editable: true,
	  droppable: true, // this allows things to be dropped onto the calendar
	  drop: function(arg) {
		// is the "remove after drop" checkbox checked?
		if (document.getElementById('drop-remove').checked) {
		  // if so, remove the element from the "Draggable Events" list
		  arg.draggedEl.parentNode.removeChild(arg.draggedEl);
		}
	  },
	  initialDate: yyyy+'-'+mm+'-'+dd,
		  weekNumbers: true,
		  navLinks: true, // can click day/week names to navigate views
		  editable: false,
		  selectable: false,
		  nowIndicator: true,
	      events: lessons
	});
	calendar.render();

  });
 })(jQuery);
