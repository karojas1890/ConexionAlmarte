


document.addEventListener('DOMContentLoaded', function() {
    const tipoRecuperacion = document.getElementById('tipoRecuperacion');
    const procesarBtn = document.getElementById('procesarBtn');
    const usuarioInput = document.getElementById('usuario'); 
    const emailError = document.getElementById('emailError'); 
    localStorage.removeItem('tipoUsuario');
    // Actualizar texto del boton segun seleccion
    tipoRecuperacion.addEventListener('change', function() {
        if (this.value === '1') {
            procesarBtn.innerHTML = '🔑 Recuperar Contraseña';
        } else if (this.value === '2') {
            procesarBtn.innerHTML = '👤 Recuperar Usuario';
        } else {
            procesarBtn.innerHTML = 'Continuar';
        }
    });

    // Manejar el clic del botón
    procesarBtn.addEventListener('click', function() {
        const tipo = tipoRecuperacion.value;
        const usuario = usuarioInput.value.trim();

        if (!tipo) {
            alert('Por favor selecciona qué necesitas recuperar');
            return;
        }

        if (!usuario) {
            alert('Por favor ingresa tu correo electrónico');
            return;
        }

        // Validar formato de email
        if (!isValidEmail(usuario)) {
            alert('Por favor ingresa un correo electrónico válido');
            return;
        }

        // Mostrar loading
        procesarBtn.innerHTML = '⏳ Validando...';
        procesarBtn.disabled = true;
        emailError.innerHTML = ''; 

        // Hacer fetch al backend
        fetch(RECOVERY_URL , {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario: usuario,
                tipo: tipo
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.success, data.message)
            if (data.success) {
                localStorage.setItem('tipoUsuario', data.tipo);
                
                window.location.href = PREGUNTAS_URL;
            } else {
                // Mostrar error en el div en lugar de alert
                emailError.innerHTML = `<div class="error-text">❌ ${data.message}</div>`;
                resetButton();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            emailError.innerHTML = '<div class="error-text">❌ Error de conexión</div>';
            resetButton();
        });
    });

    // Función para validar email
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Función para resetear botón
    function resetButton() {
        const tipo = document.getElementById('tipoRecuperacion').value;
        if (tipo === '1') {
            procesarBtn.innerHTML = '🔑 Recuperar Contraseña';
        } else if (tipo === '2') {
            procesarBtn.innerHTML = '👤 Recuperar Usuario';
        } else {
            procesarBtn.innerHTML = 'Continuar';
        }
        procesarBtn.disabled = false;
    }

    // También permitir enviar con Enter
    usuarioInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            procesarBtn.click();
        }
    });
});