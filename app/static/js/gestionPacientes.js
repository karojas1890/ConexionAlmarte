// Modal functions
        function openAddPatientModal() {
            document.getElementById('addPatientModal').classList.add('active');
        }

        function closeAddPatientModal() {
            document.getElementById('addPatientModal').classList.remove('active');
            document.getElementById('addPatientForm').reset();

            loadPacientes();
        }


        // Search functionality
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const patientCards = document.querySelectorAll('.patient-card');
            
            patientCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });

        // Close modal when clicking outside
        document.getElementById('addPatientModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeAddPatientModal();
            }
        });

async function submitPatient() {
  const data = {
    identificacion: document.getElementById("identification").value,
    nombre: document.getElementById("nombre").value,
    primerApellido: document.getElementById("apellido1").value,
    segundoApellido: document.getElementById("apellido2").value,
    telefono: document.getElementById("telefono").value,
    fechaNacimiento: document.getElementById("fechaNacimiento").value,
    provincia: document.getElementById("provincia").value,
    canton: document.getElementById("canton").value,
    distrito: document.getElementById("distrito").value,
    direccion: document.getElementById("direccion").value,
    edad: document.getElementById("edad").value,
    lugarTrabajo: document.getElementById("lugarTrabajo").value,
    ocupacion: document.getElementById("ocupacion").value,
    correo: document.getElementById("correo").value
    
  };

  try {
    const res = await fetch("/usuarios/crear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (!res.ok) {
      alert("Error: " + result.error);
       showModal('Error: ', result.error, 'error');
  
      return;
    }
    showModal('¡Usuario creado!', 'Usuario creado con exito.', 'success');
  
    document.getElementById("addPatientForm").reset();
    closeAddPatientModal();
   

  } catch (error) {
    console.error("Error al crear usuario:", error);
   
    showModal('¡Error!', error, 'error');
  
  }
}


   $(document).ready(function () {

  // 🔹 Cargar países al cargar la página
  cargarPaises();

  // 🔹 Cuando cambia el país → cargar provincias
  $("#pais").on("change", function () {
    const paisId = $(this).val();
    $("#provincia").empty();
    $("#canton").empty();
    $("#distrito").empty();

    if (paisId) {
      cargarProvincias(paisId);
    }
  });

  // 🔹 Cuando cambia la provincia → cargar ciudades
  $("#provincia").on("change", function () {
    const provinciaId = $(this).val();
    $("#canton").empty();
    $("#distrito").empty();

    if (provinciaId) {
      cargarCiudades(provinciaId);
    }
  });

  // 🔹 Cuando cambia la ciudad → cargar barrios
  $("#canton").on("change", function () {
    const ciudadId = $(this).val();
    $("#distrito").empty();

    if (ciudadId) {
      cargarBarrios(ciudadId);
    }
  });
});


//  Funciones AJAX


function cargarPaises() {
  $.ajax({
    url: PAIS_URL,
    method: "GET",
    success: function (response) {
      const select = $("#pais");
      select.empty().append('<option value="">Seleccione un país</option>');
      response.forEach(p => {
        select.append(`<option value="${p.id}">${p.nombre}</option>`);
      });
    },
    error: function (xhr) {
      console.error("Error al cargar países:", xhr.responseText);
    }
  });
}

function cargarProvincias(paisId) {
  $.ajax({
    url: PROVINCIA_URL,
    method: "GET",
    data: { pais_id: paisId },
    success: function (response) {
      const select = $("#provincia");
      select.empty().append('<option value="">Seleccione una provincia</option>');
      response.forEach(p => {
        select.append(`<option value="${p.id}">${p.nombre}</option>`);
      });
    },
    error: function (xhr) {
      console.error("Error al cargar provincias:", xhr.responseText);
    }
  });
}

function cargarCiudades(provinciaId) {
  $.ajax({
    url: CIUDAD_URL,
    method: "GET",
    data: { estado_id: provinciaId },
    success: function (response) {
      const select = $("#canton");
      select.empty().append('<option value="">Seleccione una ciudad</option>');
      response.forEach(c => {
        select.append(`<option value="${c.id}">${c.nombre}</option>`);
      });
    },
    error: function (xhr) {
      console.error("Error al cargar ciudades:", xhr.responseText);
    }
  });
}

    
function cargarBarrios(ciudadId) {
  $.ajax({
    url: BARRIO_URL,
    method: "GET",
    data: { ciudad_id: ciudadId },
    success: function (response) {
      const select = $("#distrito");
      select.empty().append('<option value="">Seleccione un barrio</option>');
      response.forEach(b => {
        select.append(`<option value="${b.id}">${b.nombre}</option>`);
      });
    },
    error: function (xhr) {
      console.error("Error al cargar barrios:", xhr.responseText);
    }
  });
}
 


  async function loadPacientes() {
    const grid = document.getElementById("patientsGrid");

    fetch(PATIENTS_URL)
    .then(response => {
        if (!response.ok) throw new Error("Error al cargar los pacientes");
        return response.json();
    })
    .then(pacientes => {
        grid.innerHTML = ""; 
       console.log(pacientes)
        pacientes.forEach(p => {
            // Crear avatar con iniciales
            const avatar = p.nombre.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();

            const card = `
            <div class="patient-card">
                <div class="patient-header">
                    <div class="patient-avatar">${avatar}</div>
                    <div class="patient-info">
                        <h3>${p.nombre}</h3>
                        <p>${p.edad} años</p>
                    </div>
                </div>
                <div class="patient-details">
                    <div class="detail-row">
                        <span class="detail-icon">
                            <!-- icono email -->
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                            </svg>
                        </span>
                        <span>${p.correo}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-icon">
                            <!-- icono telefono -->
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"></path>
                            </svg>
                        </span>
                        <span>${p.telefono}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-icon">
                            <!-- icono calendario -->
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                        </span>
                        <span>Última cita: ${p.ultima_cita || "Sin cita"}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-icon">
                            <!-- icono sesiones -->
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <line x1="12" y1="18" x2="12" y2="12"></line>
                                <line x1="9" y1="15" x2="15" y2="15"></line>
                            </svg>
                        </span>
                        <span>${p.sesiones || 0} sesiones completadas</span>
                    </div>
                </div>
                <div class="patient-actions">
                    <button class="btn-action">Ver Perfil</button>
                    <button class="btn-action">Historial</button>
                    <button class="btn-action">Editar</button>
                </div>
            </div>
            `;

            grid.insertAdjacentHTML("beforeend", card);
        });
    })
    .catch(err => {
        console.error(err);
        grid.innerHTML = "<p>Error al cargar los pacientes.</p>";
    });
}
document.addEventListener("DOMContentLoaded", loadPacientes);