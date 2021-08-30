/*const searchbar = document.querySelector('#searchbar');
const datalist = document.querySelector('#datalist')

searchbar.addEventListener('input', searchbarAPI)

function searchbarAPI(e) {
  $.ajax({
        data        : {"value": searchbar.value}, // our form data
        dataType    : 'json', // what type of data do we expect back from the server
        url         : '/api/student_searchbar',
        success     : successFunction,
        error       : errorFunction
      });
}

function successFunction(message) {
  var response = JSON.parse(message)
  for (var i = 0; i < response.length; i++){
    var option = document.createElement("option")
    option.value = "/student/employee/" + response[i].id + "/"
    option.label = response[i].name
    datalist.append(option)
  }
}

function errorFunction(e) {
}*/
