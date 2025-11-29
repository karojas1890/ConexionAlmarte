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
// Formateo de número de tarjeta
document.querySelector('input[placeholder="1234 5678 9012 3456"]').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
});

// Función principal al confirmar pago
async function continueToPaymentForm() {
    // Datos de la cita desde localStorage  cardHolderName
    const servicio = parseInt(localStorage.getItem("selectedServiceId"));
    const iddisponibilidad = parseInt(localStorage.getItem("idDisponibilidadSeleccionada"));
    const selectedDate = localStorage.getItem("selectedDate");
    const selectedTime = localStorage.getItem("selectedTime");
    const selectedPrice = parseFloat(localStorage.getItem("selectedPrice")) || 0;
    const nombre = localStorage.getItem("cardHolderName");
    // Datos de la tarjeta
    const cardNumber = document.querySelector('input[placeholder="1234 5678 9012 3456"]').value.trim();
    const cardMonth = document.querySelector('input[placeholder="MM"]').value.trim();
    const cardYear = document.querySelector('input[placeholder="AA"]').value.trim();
    const cardCVV = document.querySelector('input[placeholder="123"]').value.trim();
    const token = document.querySelector('input[placeholder="Ingrese el token"]').value.trim();

    // Preparar objeto de pago
    const tarjetaData = {
        cardNumber,
        cardHolder: nombre, 
        cvv: cardCVV,
        monto: selectedPrice
    };

    try {
        // 1️Validar tarjeta con endpoint Flask /pay
        const payRes = await fetch(PAY_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tarjetaData)
        });

        const payData = await payRes.json();

        if (!payData.success) {
            alert("Pago fallido: " + payData.message);
            return; // detener proceso si el pago falla
        }

        //Preparar objeto de cita
        const citaData = {
            usuario,
            servicio,
            iddisponibilidad,
            estado: 1,  // confirmado
            pago: 1,    // pago con tarjeta
            fecha: selectedDate,
            hora: selectedTime,
            precio: selectedPrice,
            tarjeta: {
                numero: cardNumber,
                mes: cardMonth,
                año: cardYear,
                cvv: cardCVV,
                token
            }
        };

        //Crear la cita solo si el pago fue exitoso
        const citaRes = await fetch(CITA_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(citaData)
        });

        const citaDataRes = await citaRes.json();

        if (citaDataRes.error) {
            alert("Error al procesar la cita: " + citaDataRes.error);
        } else {
            localStorage.setItem("fechaCalendario", selectedDate);
            localStorage.setItem("horaInicioCalendario", selectedTime);
            localStorage.setItem("horaFinCalendario", selectedTime);

            showConfirmationModal(selectedDate, selectedTime, selectedPrice);
        }

    } catch (err) {
        console.error("Error en pago o cita:", err);
        alert("Ocurrió un error, intenta nuevamente.");
    }
}

// Modal de confirmación
function showConfirmationModal(fecha, hora, precio) {
    const modal = document.createElement('div');
    modal.innerHTML = `
        <div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000;">
            <div style="background: white; border-radius: 15px; padding: 30px; max-width: 320px; text-align: center;">
                <div style="width: 60px; height: 60px; background: #4CAF50; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; color:white; font-size:30px;">✓</div>
                <h3>Cita confirmada!</h3>
                <p>Tu cita ha sido agendada exitosamente. Te enviaremos los detalles por email.</p>
                <div style="background:#f5f5f5; padding:15px; border-radius:8px; margin:15px 0; text-align:left;">
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
 function goToManageCards() {
            window.location.href = ADDCARD_URL;
        }

document.addEventListener("DOMContentLoaded", () => {
    const cardData = localStorage.getItem("selectedCard");
    if (!cardData) return; // Si no hay datos, no hace nada

    const card = JSON.parse(cardData);

    // Llena los campos
    const cardNumberInput = document.querySelector('input[placeholder="1234 5678 9012 3456"]');
    const expMonthInput = document.querySelector('input[placeholder="MM"]');
    const expYearInput = document.querySelector('input[placeholder="AA"]');

    if (cardNumberInput && card.ultimo4) {
        // Solo muestra los últimos 4, por seguridad
        cardNumberInput.value = `•••• •••• •••• ${card.ultimo4}`;
    }

    if (card.fecha_expiracion) {
        const [month, year] = card.fecha_expiracion.split('/');
        if (expMonthInput) expMonthInput.value = month;
        if (expYearInput) expYearInput.value = year;
    }

});
