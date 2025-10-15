


        function goBack(button) {
            const goBackURl = button.getAttribute('data-url');
            window.location.href = goBackURl ;
        }

        // function continueToPaymentForm(button) {
        //     const selectedPayment = document.querySelector('.payment-option.selected .payment-text')?.textContent;
        //     localStorage.setItem('selectedPayment', selectedPayment);
        //     const paymentforUrl = button.getAttribute('data-url');
        //     // If credit card is selected, go to payment form, otherwise show confirmation
        //     if (selectedPayment === 'Tarjeta de crédito o débito') {
        //         window.location.href = paymentforUrl;
        //     } else {
        //         showConfirmation();
        //     }
        // }

        function showConfirmation() {
    // Tomar datos del localStorage
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
     document.addEventListener("DOMContentLoaded", () => {
    // Servicio
    const selectedService = localStorage.getItem('selectedServiceName');
    const selectedPrice = parseFloat(localStorage.getItem('selectedPrice'));

    const serviceText = document.getElementById('service-summary-text');
    const priceText = document.getElementById('summary-price');
    const dateText = document.getElementById('summary-date');
    const timeText = document.getElementById('summary-time');

    // Muestra el servicio y el precio
    if (selectedService) {
        serviceText.textContent = selectedService;
        priceText.textContent = `₡${!isNaN(selectedPrice) ? selectedPrice.toLocaleString() : "N/A"}`;
    } else {
        serviceText.textContent = "No has seleccionado un servicio aún";
        priceText.textContent = "₡0";
    }

    // Fecha y hora
    const selectedDate = localStorage.getItem("selectedDate");
    const selectedTime = localStorage.getItem("selectedTime");

    dateText.textContent = selectedDate;
if (selectedTime) timeText.textContent = selectedTime;
});

