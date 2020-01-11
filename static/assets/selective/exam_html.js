

var time = document.getElementById('timer').getAttribute("time-left");
function countdowntimer()
{   
    if (time>0){
        time -=1;
        hour = Math.floor(time/3600);
        minute = Math.floor(time/60);
        seconds = time%60
        document.getElementById("countdowntime").innerText =  String(hour)+ ":" + String(minute)+":"+String(seconds) + "   ";

    } else {
        window.location='/result';
    }       
}
setInterval(countdowntimer,1000)