 // En tu archivo code.js - VERIFICA QUE EL ELEMENTO EXISTA
document.addEventListener('DOMContentLoaded', function() {
    const resendBtn = document.getElementById('resendBtn');
    const countdownElement = document.getElementById('countdown');
    
    // Solo continuar si los elementos existen
    if (!resendBtn || !countdownElement) {
        console.error('No se encontraron los elementos del temporizador');
        return;
    }

    let timeLeft = 60;
    let countdownInterval;

    function startCountdown() {
        clearInterval(countdownInterval); 
        countdownInterval = setInterval(() => {
            timeLeft--;
            
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            countdownElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 15) {
                countdownElement.style.color = '#e74c3c';
            }
            
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                countdownElement.textContent = "00:00";
                countdownElement.style.color = '#e74c3c';
                resendBtn.disabled = false;
                resendBtn.style.opacity = "1";
                resendBtn.style.cursor = "pointer";
            }
        }, 1000);
    }

    // Iniciar temporizador
    startCountdown();

    // Event listener para reenviar
    resendBtn.addEventListener('click', function() {
        if (!this.disabled) {
            // Mostrar loading
            const originalText = this.textContent;
            this.textContent = 'Enviando...';
            this.disabled = true;
            
            fetch(REENVIAR_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin' // Incluir cookies/session
            })
            .then(response => {
                // Verificar si la respuesta es JSON
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    throw new TypeError('La respuesta no es JSON');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    
                    // Reiniciar temporizador
                    timeLeft = 60;
                    countdownElement.style.color = '#2c3e50';
                    countdownElement.textContent = '01:00';
                    resendBtn.disabled = true;
                    resendBtn.style.opacity = "0.5";
                    resendBtn.textContent = originalText;
                    startCountdown();
                } else {
                   
                    resendBtn.disabled = false;
                    resendBtn.style.opacity = "1";
                    resendBtn.textContent = originalText;
                }
            })
            .catch(error => {
               
                resendBtn.disabled = false;
                resendBtn.style.opacity = "1";
                resendBtn.textContent = originalText;
            });
        }
    });
});


         document.getElementById('securityCode').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            e.target.value = value;
        });