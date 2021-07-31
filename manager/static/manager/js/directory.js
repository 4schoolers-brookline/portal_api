var select = document.querySelector('#select_active');

var all_students = document.querySelector('#all_students-div');
var active_students = document.querySelector('#active_students-div');
var inactive_students = document.querySelector('#inactive_students-div');


select.addEventListener("change", select_function)
function select_function(e) {
  var value = select.value
  if (value == "All Students"){
    all_students.style.display = ""
    active_students.style.display = "none"
    inactive_students.style.display = "none"
  }
  if (value == "Active"){
    all_students.style.display = "none"
    active_students.style.display = ""
    inactive_students.style.display = "none"
  }
  if (value == "None Active"){
    all_students.style.display = "none"
    active_students.style.display = "none"
    inactive_students.style.display = ""
  }
}
