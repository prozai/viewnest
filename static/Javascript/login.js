function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    var toggleBtnIcon = document.querySelector('.peek-btn i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtnIcon.classList.remove('fa-eye');
        toggleBtnIcon.classList.add('fa-eye-slash'); // Change to hide icon
    } else {
        passwordInput.type = 'password';
        toggleBtnIcon.classList.remove('fa-eye-slash');
        toggleBtnIcon.classList.add('fa-eye'); // Change back to show icon
    }
}