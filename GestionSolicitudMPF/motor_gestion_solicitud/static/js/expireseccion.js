function redirectToLogin() {
    window.location.href = "/"; 
}

var inactivityTime = 5 * 60 * 1000; 


var lastActivityTime = new Date().getTime();


function checkUserActivity() {
    var currentTime = new Date().getTime();
    var elapsedTime = currentTime - lastActivityTime;
    if (elapsedTime > inactivityTime) {
        redirectToLogin();  
    }
}

document.addEventListener("mousemove", function() {
    lastActivityTime = new Date().getTime();  
});

document.addEventListener("keypress", function() {
    lastActivityTime = new Date().getTime();  
});

setInterval(checkUserActivity, 1000); 