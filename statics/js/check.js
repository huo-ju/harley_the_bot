
var xhr = new XMLHttpRequest();

xhr.onload = function () {
	if (xhr.status >= 200 && xhr.status < 300) {
        data = JSON.parse(xhr.response);
        document.getElementById("task_status").textContent=data.state;
        if(data.state =="SUCCESS"){
            window.location = "/idenresult?task_id="+task_id;
        }
	} else {
		console.log('The request failed!');
	}
};



var checktimer = setInterval(check_status, 1000);
function check_status() {
  xhr.open('GET', '/api/check?task_id='+task_id);
  xhr.send();
}
