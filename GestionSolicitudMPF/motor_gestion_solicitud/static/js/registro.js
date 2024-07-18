function togglePasswordVisibility(inputId, eyeIconId) {
    var passwordInput = document.getElementById(inputId);
    var eyeIcon = document.getElementById(eyeIconId);
    
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}