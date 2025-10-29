  // Sample data - Replace with actual API call
        const activityTypes = {
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

        let currentPage = 1;
        const itemsPerPage = 10;
        let allActivities = [];
        let filteredActivities = [];

        // Load activities from API
        async function loadActivities() {
    try {
        // Llamada a la API real
        const response = await fetch(AUDITORIA_URL); // tu endpoint Flask
        const result = await response.json();

        // Mapear los datos a tu formato JS
        allActivities = result.map(a => ({
            id_actividad: a.id_actividad,
            identificacion_consultante: a.identificacion_consultante,
            tipo_actividad: a.tipo_actividad,
            descripcion: a.descripcion || "",
            codigo: a.codigo,
            fecha: a.fecha,
            ip_origen: a.ip_origen || "",
            dispositivo: a.dispositivo || "Desconocido",
            ubicacion: a.ubicacion || "",
            datos_modificados: a.datos_modificados,
            exito: a.exito === true,
        }));

        filteredActivities = [...allActivities];
        updateStats();
        renderActivities();
    } catch (error) {
        console.error('Error loading activities:', error);
    }
}


        // Generate sample data
        function generateSampleData() {
            const data = [];
            const now = new Date();
            
            for (let i = 0; i < 50; i++) {
                const date = new Date(now - Math.random() * 7 * 24 * 60 * 60 * 1000);
                const type = Math.floor(Math.random() * 10) + 1;
                const success = Math.random() > 0.2;
                
                data.push({
                    id_actividad: i + 1,
                    identificacion_consultante: `${Math.floor(Math.random() * 900000000) + 100000000}`,
                    tipo_actividad: type,
                    descripcion: `Descripción de la actividad ${activityTypes[type]}`,
                    codigo: success ? null : `ERR${Math.floor(Math.random() * 1000)}`,
                    fecha: date.toISOString(),
                    ip_origen: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
                    dispositivo: ['Chrome/Windows', 'Safari/iOS', 'Firefox/Linux', 'Edge/Windows'][Math.floor(Math.random() * 4)],
                    ubicacion: ['San José, CR', 'Heredia, CR', 'Alajuela, CR', 'Cartago, CR'][Math.floor(Math.random() * 4)],
                    datos_modificados: type === 6 ? { campo: 'email', anterior: 'old@email.com', nuevo: 'new@email.com' } : null,
                    exito: success
                });
            }
            
            return data.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
        }

        // Update statistics
        function updateStats() {
    const success = filteredActivities.filter(a => a.exito).length;
    const errors = filteredActivities.filter(a => !a.exito && a.tipo_actividad !== 9).length;
    const warnings = filteredActivities.filter(a => a.tipo_actividad === 9).length;
    
    document.getElementById('totalSuccess').textContent = success;
    document.getElementById('totalErrors').textContent = errors;
    document.getElementById('totalWarnings').textContent = warnings;
    document.getElementById('totalActivities').textContent = filteredActivities.length;
}


        // Render activities
        function renderActivities() {
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageActivities = filteredActivities.slice(start, end);
            
            const listContainer = document.getElementById('activityList');
            
            if (pageActivities.length === 0) {
                listContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📋</div>
                        <h3>No se encontraron registros</h3>
                        <p>No hay actividades que coincidan con los filtros seleccionados</p>
                    </div>
                `;
                document.getElementById('pagination').innerHTML = '';
                return;
            }
            
            listContainer.innerHTML = pageActivities.map(activity => {
                const date = new Date(activity.fecha);
                const dateStr = date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
                const timeStr = date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
                
                return `
                    <div class="activity-item" onclick="toggleDetails(${activity.id_actividad})">
                        <div class="activity-header">
                            <div class="activity-main">
                                <div class="activity-title">
                                    <span class="activity-badge ${activity.exito ? 'badge-success' : 'badge-error'}">
                                        ${activity.exito ? 'Exitoso' : 'Fallido'}
                                    </span>
                                    <span class="activity-type">${activityTypes[activity.tipo_actividad]}</span>
                                </div>
                                <div class="activity-description">${activity.descripcion}</div>
                                <div class="activity-meta">
                                    <span class="activity-meta-item">👤 ${activity.identificacion_consultante}</span>
                                    <span class="activity-meta-item">📍 ${activity.ip_origen}</span>
                                    <span class="activity-meta-item">💻 ${activity.dispositivo}</span>
                                </div>
                            </div>
                            <div class="activity-time">
                                <span class="activity-date">${dateStr}</span>
                                <span class="activity-timestamp">${timeStr}</span>
                            </div>
                        </div>
                        <div class="activity-details" id="details-${activity.id_actividad}">
                            <div class="details-grid">
                                <div class="detail-item">
                                    <div class="detail-label">ID de Actividad</div>
                                    <div class="detail-value">${activity.id_actividad}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Identificación</div>
                                    <div class="detail-value">${activity.identificacion_consultante}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">IP de Origen</div>
                                    <div class="detail-value">${activity.ip_origen}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Dispositivo</div>
                                    <div class="detail-value">${activity.dispositivo}</div>
                                </div>
                                ${activity.ubicacion ? `
                                <div class="detail-item">
                                    <div class="detail-label">Ubicación</div>
                                    <div class="detail-value">${activity.ubicacion}</div>
                                </div>
                                ` : ''}
                                ${activity.codigo ? `
                                <div class="detail-item">
                                    <div class="detail-label">Código</div>
                                    <div class="detail-value">${activity.codigo}</div>
                                </div>
                                ` : ''}
                            </div>
                            ${activity.datos_modificados ? `
                            <div class="json-data">
                                <strong>Datos Modificados:</strong><br>
                                ${JSON.stringify(activity.datos_modificados, null, 2)}
                            </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            }).join('');
            
            renderPagination();
        }

        // Toggle activity details
        function toggleDetails(id) {
            const item = event.currentTarget;
            item.classList.toggle('expanded');
        }

        // Render pagination
        function renderPagination() {
            const totalPages = Math.ceil(filteredActivities.length / itemsPerPage);
            const paginationContainer = document.getElementById('pagination');
            
            if (totalPages <= 1) {
                paginationContainer.innerHTML = '';
                return;
            }
            
            let html = `
                <button onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
                    ← Anterior
                </button>
            `;
            
            for (let i = 1; i <= totalPages; i++) {
                if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
                    html += `
                        <button onclick="changePage(${i})" class="${i === currentPage ? 'active' : ''}">
                            ${i}
                        </button>
                    `;
                } else if (i === currentPage - 2 || i === currentPage + 2) {
                    html += '<span>...</span>';
                }
            }
            
            html += `
                <button onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
                    Siguiente →
                </button>
            `;
            
            paginationContainer.innerHTML = html;
        }

        // Change page
        function changePage(page) {
            currentPage = page;
            renderActivities();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Apply filters
        function applyFilters() {
            const userFilter = document.getElementById('filterUser').value.toLowerCase();
            const typeFilter = document.getElementById('filterType').value;
            const statusFilter = document.getElementById('filterStatus').value;
            const dateFromFilter = document.getElementById('filterDateFrom').value;
            const dateToFilter = document.getElementById('filterDateTo').value;
            
            filteredActivities = allActivities.filter(activity => {
                if (userFilter && !activity.identificacion_consultante.toLowerCase().includes(userFilter)) {
                    return false;
                }
                if (typeFilter && activity.tipo_actividad.toString() !== typeFilter) {
                    return false;
                }
                if (statusFilter && activity.exito.toString() !== statusFilter) {
                    return false;
                }
                if (dateFromFilter) {
                    const activityDate = new Date(activity.fecha).toISOString().split('T')[0];
                    if (activityDate < dateFromFilter) {
                        return false;
                    }
                }
                if (dateToFilter) {
                    const activityDate = new Date(activity.fecha).toISOString().split('T')[0];
                    if (activityDate > dateToFilter) {
                        return false;
                    }
                }
                return true;
            });
            
            currentPage = 1;
            updateStats();
            renderActivities();
        }

        // Clear filters
        function clearFilters() {
            document.getElementById('filterUser').value = '';
            document.getElementById('filterType').value = '';
            document.getElementById('filterStatus').value = '';
            document.getElementById('filterDateFrom').value = '';
            document.getElementById('filterDateTo').value = '';
            
            filteredActivities = [...allActivities];
            currentPage = 1;
            updateStats();
            renderActivities();
        }

        // Export to CSV
        function exportToCSV() {
            const headers = ['ID', 'Identificación', 'Tipo', 'Descripción', 'Fecha', 'IP', 'Dispositivo', 'Ubicación', 'Estado'];
            const rows = filteredActivities.map(a => [
                a.id_actividad,
                a.identificacion_consultante,
                activityTypes[a.tipo_actividad],
                a.descripcion,
                new Date(a.fecha).toLocaleString('es-ES'),
                a.ip_origen,
                a.dispositivo,
                a.ubicacion || '',
                a.exito ? 'Exitoso' : 'Fallido'
            ]);
            
            let csv = headers.join(',') + '\n';
            rows.forEach(row => {
                csv += row.map(cell => `"${cell}"`).join(',') + '\n';
            });
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `auditoria_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
        }

        // Initialize
        loadActivities();