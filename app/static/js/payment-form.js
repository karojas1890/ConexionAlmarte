 function goBack(button) {
            const goBackURl = button.getAttribute('data-url');
            window.location.href = goBackURl ;
        }
        function processPayment() {
            // Show confirmation modal
           const selectedService = localStorage.getItem('selectedServiceName') || "No seleccionado";
    const selectedPrice = parseFloat(localStorage.getItem('selectedPrice')) || 0;
    const selectedDate = localStorage.getItem('selectedDate') || "No definida";
    const selectedTime = localStorage.getItem('selectedTime') || "No definida";

    // Crear modal
    const modal = document.createElement('div');
    modal.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
            <div style="background: white; border-radius: 15px; padding: 30px; max-width: 300px; text-align: center; margin: 20px;">
                <div style="width: 60px; height: 60px; background: #4CAF50; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 30px;">✓</div>
                <h3 style="color: #333; margin-bottom: 15px; font-size: 18px;">¡Cita confirmada!</h3>
                <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Tu cita ha sido agendada exitosamente. Te enviaremos los detalles por email.</p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left;">
                    <h4 style="color: #333; font-size: 14px; margin-bottom: 10px;">Detalles de tu cita</h4>
                    <p style="font-size: 12px; color: #666; margin-bottom: 5px;">${selectedService}</p>
                    <p style="font-size: 12px; color: #666; margin-bottom: 5px;">${selectedDate}, ${selectedTime}</p>
                    <p style="font-size: 12px; color: #666;">Total: ₡${selectedPrice.toLocaleString()}</p>
                </div>
                <button onclick="closeModal()" style="background: #5f9ea0; color: white; border: none; border-radius: 20px; padding: 12px 30px; font-size: 14px; cursor: pointer;">Entendido</button>
            </div>
        </div>
    `;
            document.body.appendChild(modal);
        }

        function closeModal() {
            const modal = document.querySelector('[style*="position: fixed"]');
            
            if (modal) {
                modal.remove();
                 window.location.href = dashboardUrl;
            }
        }

        // Format card number input
        document.querySelector('input[placeholder="1234 5678 9012 3456"]').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });