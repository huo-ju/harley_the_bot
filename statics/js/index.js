document.getElementById('submit_screen_name').addEventListener("click", function(){ 
  event.preventDefault();
  console.log("something"); 
  idensubmit();
  return false; 
},false);

function idensubmit() {
    document.getElementById('submit_progressbar').style.display = "block";
    document.getElementById('idenform').submit();
    document.getElementById('submit_screen_name').disabled=true;
    document.getElementById('screen_name').disabled=true;

}
