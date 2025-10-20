


        function goBack(button) {
            const goBackURl = button.getAttribute('data-url');
            window.location.href = goBackURl ;
        }


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

function mostrarModalCalendario() {
    const modal = document.getElementById("calendarModal");
    modal.classList.remove("hidden");

    document.getElementById("btnSiCalendario").onclick = () => {
        modal.classList.add("hidden");
        agregarCitaAlCalendario(); 
        setTimeout(() => {
        showConfirmation();
    }, 1000);       
    };

    document.getElementById("btnNoCalendario").onclick = () => {
        modal.classList.add("hidden");
        showConfirmation();       
    };
}



function agregarCitaAlCalendario() {
  const selectedDate = localStorage.getItem("fechaInicioICS");
  const selectedTime = localStorage.getItem("fechaFinICS");
  const selectedServiceName = localStorage.getItem("selectedServiceName");

  //console.log({ selectedDate, selectedTime, selectedServiceName });

//   if (!selectedDate || !selectedTime || !selectedServiceName) {
//     alert("No hay datos suficientes para agregar la cita.");
//     return;
//   }

  const start = new Date(`${selectedDate}T${selectedTime}`);
  if (isNaN(start.getTime())) {
    console.error("Fecha inválida:", selectedDate, selectedTime);
    alert("No se pudo generar la cita por formato de fecha/hora incorrecto.");
    return;
  }

  const end = new Date(start.getTime() + 30 * 60000);

  const eventoICS = `
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Conexion//Agenda//ES
BEGIN:VEVENT
SUMMARY:${selectedServiceName}
DTSTART:${start.toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DTEND:${end.toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DESCRIPTION:Cita agendada en tu calendario
END:VEVENT
END:VCALENDAR
  `.trim();

  const blob = new Blob([eventoICS], { type: "text/calendar" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${selectedServiceName}_cita.ics`;
  a.click();
  URL.revokeObjectURL(url);
}