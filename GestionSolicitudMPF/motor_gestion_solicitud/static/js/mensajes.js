document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var messages = document.querySelector('.messages-container');
        if (messages) {
            messages.style.display = 'none';
        }
    }, 5000); 
});