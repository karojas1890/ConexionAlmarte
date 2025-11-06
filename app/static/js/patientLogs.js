async function cargarActividades() {
    const response = await fetch(AUDITORIAP_URL);
    const data = await response.json();

    const container = document.getElementById('activitiesContainer');
    container.innerHTML = ''; // Limpia la lista actual

    data.data.forEach(a => {
        const statusClass = a.exito ? 'success' : 'failed';
        const tipoActividad = getActivityName(a.tipo_actividad);

        const item = document.createElement('div');
        item.classList.add('almarte-activity-item');
        item.innerHTML = `
            <div class="almarte-activity-header-item" onclick="toggleDetails(this)">
                <div class="almarte-activity-title">
                    <div class="almarte-activity-icon ${statusClass}">🔹</div>
                    <div class="almarte-activity-info">
                        <h3>${tipoActividad}</h3>
                        <p>${a.descripcion || 'Sin descripción'}</p>
                        <span class="almarte-activity-status ${statusClass}">
                            ${a.exito ? 'Exitoso' : 'Fallido'}
                        </span>
                    </div>
                </div>
                <div class="almarte-activity-time">
                    ${new Date(a.fecha).toLocaleString()}
                </div>
            </div>
            <div class="almarte-activity-details">
                <div class="almarte-detail-row">
                    <span class="almarte-detail-label">IP:</span>
                    <span class="almarte-detail-value">${a.ip_origen || 'N/A'}</span>
                </div>
                <div class="almarte-detail-row">
                    <span class="almarte-detail-label">Dispositivo:</span>
                    <span class="almarte-detail-value">${a.dispositivo || 'N/A'}</span>
                </div>
                <div class="almarte-detail-row">
                    <span class="almarte-detail-label">Ubicación:</span>
                    <span class="almarte-detail-value">${a.ubicacion || 'N/A'}</span>
                </div>
            </div>
        `;
        container.appendChild(item);
    });
}

function getActivityName(tipo) {
    const tipos = {
            1: 'Inicio de Sesión',
            2: 'Cita reservada',
            3: 'Registro de Usuario',
            4: 'Recuperación de Contraseña',
            5: 'Cambio de Contraseña',
            6: 'Actualización de Perfil',
            7: 'Login Exitoso',
            8: 'Cancelación de Cita',
            9: 'Recuperacion de Usuario',
            10: 'Cambio de contrasena',
            11:'Error de Login',
            12:'Bloqueo por ecxeso de intentos'
    };
    return tipos[tipo] || "Actividad";
}
 function toggleDetails(element) {
            element.classList.toggle('expanded');
        }

        function filterActivities() {
            const activityType = document.getElementById('activityType').value;
            const dateFrom = document.getElementById('dateFrom').value;
            const dateTo = document.getElementById('dateTo').value;
            const status = document.getElementById('statusFilter').value;

            console.log('Filtros aplicados:', {
                activityType,
                dateFrom,
                dateTo,
                status
            });
        }

        function resetFilters() {
            document.getElementById('activityType').value = '';
            document.getElementById('dateFrom').value = '';
            document.getElementById('dateTo').value = '';
            document.getElementById('statusFilter').value = '';
        }

        function previousPage() {
            console.log('Página anterior');
        }

        function nextPage() {
            console.log('Página siguiente');
        }
// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", cargarActividades);
