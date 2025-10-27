let disponibilidadGlobal = {}; 
let nuevosSlots = [];
let fechaSeleccionada = null;

const monthNames = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

//  Genera el calendario
function generarCalendario(year, month) {
  const calendarDays = document.getElementById("calendar-days");
  calendarDays.innerHTML = "";
  document.getElementById("calendar-month").textContent = `${monthNames[month]} ${year}`;

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  for (let i = 0; i < firstDay; i++) {
      const div = document.createElement("div");
      div.classList.add("day");
      calendarDays.appendChild(div);
  }

  for (let d = 1; d <= daysInMonth; d++) {
      const div = document.createElement("div");
      div.classList.add("day");
      div.innerHTML = `<span class="day-number">${d}</span>`;

      const fecha = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const estadoDia = obtenerEstadoDia(fecha);

      if (estadoDia === "available") div.classList.add("available");
      else if (estadoDia === "partially-available") div.classList.add("partially-available");
      else if (estadoDia === "unavailable") div.classList.add("unavailable");

      div.addEventListener("click", () => seleccionarDia(fecha, div));
      calendarDays.appendChild(div);
  }
}

// Determina el color de cada día según los slots disponibles
function obtenerEstadoDia(fecha) {
  const slots = disponibilidadGlobal[fecha] || [];
  if (slots.length === 0) return null;
  const activos = slots.filter(s => s.estado === 1).length;
  if (activos === 0) return "unavailable";
  if (activos < 8) return "partially-available";
  return "available";
}

//  Mostrar slots del día seleccionado
async function seleccionarDia(fecha, elemento) {
  document.querySelectorAll(".day").forEach(d => d.classList.remove("selected"));
  elemento.classList.add("selected");
  fechaSeleccionada = fecha;
  document.getElementById("selected-date").textContent = fecha;
  await cargarSlots(fecha);
}

// 📡 Cargar disponibilidades y mostrar slots
async function cargarSlots(fecha) {
  const slotsList = document.getElementById("time-slots-list");
  slotsList.innerHTML = "";
  nuevosSlots = [];

  if (Object.keys(disponibilidadGlobal).length === 0) {
      const res = await fetch(AVAILABILITY_URL);
      const data = await res.json();
      disponibilidadGlobal = data.reduce((acc, slot) => {
          if (!acc[slot.fecha]) acc[slot.fecha] = [];
          acc[slot.fecha].push(slot);
          return acc;
      }, {});
  }

  const slotsBase = [
      "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
      "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
  ];

  slotsBase.forEach(time => {
      const div = document.createElement("div");
      div.classList.add("time-slot");
      div.innerHTML = `<span class="slot-time">${time}</span><div class="slot-toggle"></div>`;

      const encontrado = (disponibilidadGlobal[fecha] || []).find(s => `${s.hora_inicio} - ${s.hora_fin}` === time);
      if (encontrado) {
          div.querySelector(".slot-toggle").classList.add("active");
          div.classList.add("occupied");
      }

      div.querySelector(".slot-toggle").addEventListener("click", function() {
          if (div.classList.contains("occupied")) return;
          this.classList.toggle("active");
          const [inicio, fin] = time.split(" - ");
          if (this.classList.contains("active")) {
              nuevosSlots.push({ hora_inicio: inicio, hora_fin: fin });
          } else {
              nuevosSlots = nuevosSlots.filter(s => !(s.hora_inicio === inicio && s.hora_fin === fin));
          }
      });

      slotsList.appendChild(div);
  });
}

// 💾 Guardar slots nuevos
document.getElementById("save-slots-btn").addEventListener("click", async () => {
  if (!fechaSeleccionada || nuevosSlots.length === 0) return alert("Seleccione al menos un horario");
  await fetch("{{ url_for('availability.AgregarDisponibilidad') }}", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slots: nuevosSlots.map(s => ({
            fecha: fechaSeleccionada,  
            hora_inicio: s.hora_inicio,
            hora_fin: s.hora_fin
        }))
    })
  });
  alert("Disponibilidad guardada correctamente");
  await cargarSlots(fechaSeleccionada);
  generarCalendario(currentYear, currentMonth);
  window.location.reload();
});

// 🔄 Navegación entre meses
let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

document.getElementById("prev-month").addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) { currentMonth = 11; currentYear--; }
  generarCalendario(currentYear, currentMonth);
});

document.getElementById("next-month").addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) { currentMonth = 0; currentYear++; }
  generarCalendario(currentYear, currentMonth);
});

// Inicializar
generarCalendario(currentYear, currentMonth);