// Mostrar resumen de la cita al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    const selectedService = localStorage.getItem('selectedServiceName') || "No seleccionado";
    const selectedPrice = parseFloat(localStorage.getItem('selectedPrice')) || 0;
    const selectedDate = localStorage.getItem("selectedDate") || "No definida";
    const selectedTime = localStorage.getItem("selectedTime") || "No definida";

    document.getElementById('service-summary-text').textContent = selectedService;
    document.getElementById('summary-price').textContent = `₡${!isNaN(selectedPrice) ? selectedPrice.toLocaleString() : "0"}`;
    document.getElementById('summary-date').textContent = selectedDate;
    document.getElementById('summary-time').textContent = selectedTime;
});

// Variable global para guardar la opción de pago
window.selectedPayment = 'Tarjeta de crédito o débito'; // por defecto

// Función para seleccionar método de pago
window.selectPayment = function(element) {
    document.querySelectorAll('.payment-option').forEach(option => option.classList.remove('selected'));
    element.classList.add('selected');
    window.selectedPayment = element.querySelector('.payment-text').innerText;
    console.log('Método de pago seleccionado:', window.selectedPayment);
}

// Función al continuar con el pago
function continueToPaymentForm() {
    
    const servicio = parseInt(localStorage.getItem("selectedServiceId"));
    const iddisponibilidad = parseInt(localStorage.getItem("idDisponibilidadSeleccionada"));
    const selectedDate = localStorage.getItem("selectedDate");
    const selectedTime = localStorage.getItem("selectedTime");
    const selectedPrice = parseFloat(localStorage.getItem("selectedPrice")) || 0;

    const citaData = {
        usuario,
        servicio,
        iddisponibilidad,
        estado: 1,  // 1 = confirmado
        pago: 1     // 1 = pago con tarjeta o efectivo según selección
    };

    if (window.selectedPayment === 'Tarjeta de crédito o débito') {
        // Redirigir al formulario de pago real
        
        window.location.href = paymentforUrl;
    } else {
        // Para efectivo, transferencia o SINPE, crear cita directamente
        fetch(CITA_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(citaData)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                // Mostrar modal de confirmación
                showConfirmation(selectedDate, selectedTime, selectedPrice);
            }
        })
        .catch(err => console.error("Error al crear cita:", err));
    }
}

// Modal de confirmación
function showConfirmation(fecha, hora, precio) {
    const selectedService = localStorage.getItem('selectedServiceName') || "Servicio no definido";

    const modal = document.createElement('div');
    modal.innerHTML = `
        <div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000;">
            <div style="background: white; border-radius: 15px; padding: 30px; max-width: 320px; text-align: center;">
                <div style="width: 60px; height: 60px; background: #4CAF50; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; color:white; font-size:30px;">✓</div>
                <h3>Cita confirmada!</h3>
                <p>Tu cita ha sido agendada exitosamente. Te enviaremos los detalles por email.</p>
                <div style="background:#f5f5f5; padding:15px; border-radius:8px; margin:15px 0; text-align:left;">
                    <p><strong>Servicio:</strong> ${selectedService}</p>
                    <p><strong>Fecha:</strong> ${fecha}</p>
                    <p><strong>Hora:</strong> ${hora}</p>
                    <p><strong>Total:</strong> ₡${precio.toLocaleString()}</p>
                </div>
                <button onclick="closeModal()" style="background:#5f9ea0; color:white; border:none; border-radius:20px; padding:12px 30px; cursor:pointer;">Entendido</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function closeModal() {
    const modal = document.querySelector('[style*="position: fixed"]');
    if (modal) modal.remove();
    window.location.href = dashboardUrl;
}
