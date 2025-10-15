// Inicializar cuando la página cargue
document.addEventListener('DOMContentLoaded', function () {
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    const emailInput = document.getElementById('email');

    // Validación en tiempo real del email
    emailInput.addEventListener('input', function () {
        clearMessages();
        this.classList.remove('error', 'success');
    });

    emailInput.addEventListener('blur', function () {
        validateEmail(this.value);
    });
}

// Validar email
function validateEmail(email) {
    const emailInput = document.getElementById('email');
    const errorMessage = document.getElementById('emailError');
    const successMessage = document.getElementById('emailSuccess');

    if (!email.trim()) {
        showError('El correo electrónico es requerido');
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('Formato de correo electrónico inválido');
        return false;
    }

    
    showSuccess('Correo válido');
    return true;

    function showError(message) {
        emailInput.classList.add('error');
        emailInput.classList.remove('success');
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
    }

    function showSuccess(message) {
        emailInput.classList.add('success');
        emailInput.classList.remove('error');
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        errorMessage.style.display = 'none';
    }
}

// Limpiar mensajes
function clearMessages() {
    document.getElementById('emailError').style.display = 'none';
    document.getElementById('emailSuccess').style.display = 'none';
}

// Auto-focus en el input al cargar
window.addEventListener('load', function () {
    document.getElementById('email').focus();
});
