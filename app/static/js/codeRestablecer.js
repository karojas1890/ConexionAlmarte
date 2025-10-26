  // Validación del código
        document.getElementById('codeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const code = document.getElementById('verificationCode').value;
            
            // Validar código con el backend
            fetch('/api/verify-recovery-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Código correcto, pasar a la siguiente sección
                    document.getElementById('step1').classList.remove('active');
                    document.getElementById('step1').classList.add('completed');
                    document.getElementById('line1').classList.add('completed');
                    document.getElementById('step2').classList.add('active');
                    
                    document.getElementById('codeSection').classList.remove('active');
                    document.getElementById('passwordSection').classList.add('active');
                    document.getElementById('codeError').classList.remove('show');
                } else {
                    // Código incorrecto
                    document.getElementById('codeError').classList.add('show');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al verificar el código. Por favor, intenta nuevamente.');
            });
        });

        // Reenviar código
        document.getElementById('resendCode').addEventListener('click', function(e) {
            e.preventDefault();
            
            fetch('/api/resend-recovery-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Se ha reenviado el código a tu correo electrónico.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        // Validación de requisitos de contraseña en tiempo real
        const newPasswordInput = document.getElementById('newPassword');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const submitButton = document.getElementById('submitPassword');

        newPasswordInput.addEventListener('input', function() {
            const password = this.value;
            
            // Validar longitud
            const lengthValid = password.length >= 8;
            toggleRequirement('req-length', lengthValid);
            
            // Validar mayúscula
            const uppercaseValid = /[A-Z]/.test(password);
            toggleRequirement('req-uppercase', uppercaseValid);
            
            // Validar minúscula
            const lowercaseValid = /[a-z]/.test(password);
            toggleRequirement('req-lowercase', lowercaseValid);
            
            // Validar número
            const numberValid = /[0-9]/.test(password);
            toggleRequirement('req-number', numberValid);
            
            // Habilitar botón si todos los requisitos se cumplen
            const allValid = lengthValid && uppercaseValid && lowercaseValid && numberValid;
            checkPasswordsMatch(allValid);
        });

        confirmPasswordInput.addEventListener('input', function() {
            const allRequirementsMet = document.querySelectorAll('.requirement.valid').length === 4;
            checkPasswordsMatch(allRequirementsMet);
        });

        function toggleRequirement(id, isValid) {
            const element = document.getElementById(id);
            if (isValid) {
                element.classList.add('valid');
            } else {
                element.classList.remove('valid');
            }
        }

        function checkPasswordsMatch(allRequirementsMet) {
            const password = newPasswordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            
            if (allRequirementsMet && password === confirmPassword && password.length > 0) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }

        // Enviar nueva contraseña
        document.getElementById('passwordForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (newPassword !== confirmPassword) {
                document.getElementById('passwordError').classList.add('show');
                return;
            }
            
            document.getElementById('passwordError').classList.remove('show');
            
            // Enviar nueva contraseña al backend
            fetch('/api/reset-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    newPassword: newPassword 
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    alert('¡Contraseña restablecida exitosamente! Serás redirigido al inicio de sesión.');
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    alert('Ocurrió un error al restablecer la contraseña. Por favor, intenta nuevamente.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al restablecer la contraseña. Por favor, intenta nuevamente.');
            });
        });

        // Solo permitir números en el código de verificación
        document.getElementById('verificationCode').addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
        });