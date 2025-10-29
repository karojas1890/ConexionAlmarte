 // Validación del código
        document.getElementById('codeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const code = document.getElementById('verificationCode').value;
            
            // Validar código con el backend
            fetch(VALIDATECODE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                  if (data.type==="2"){
                    showModal('¡Usuario recuperado!', 'Revisa el correo electronico paraverificar los datos .', 'success');
                    }
                setTimeout(() => {
                   window.location.href= data.redirect_url
                },4000)
                } else {
                    // Código incorrecto
                    document.getElementById('codeError').classList.add('show');
                }
            })
            .catch(error => {
                console.error('Error:', error);
               
                 showModal('Ocurrió un error al verificar el código', 'Por favor, intenta nuevamente.','"error"');
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
        