let encuestasData = [];
let charts = {};

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', function() {
    cargarDatosEncuestas();
    inicializarFiltros();
});

// Cargar datos de encuestas
async function cargarDatosEncuestas() {
    try {
        const response = await fetch(VERENCUESTA_URL);
        const data = await response.json();
        
        if (data.success) {
            encuestasData = data.encuestas;
            actualizarEstadisticas();
            actualizarTabla();
            inicializarGraficos();
        } else {
            console.error('Error al cargar encuestas:', data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los datos de encuestas');
    }
}

// Actualizar estadísticas
function actualizarEstadisticas() {
    const totalEncuestas = encuestasData.length;
    const promedioGeneral = encuestasData.reduce((sum, encuesta) => sum + (encuesta.promedio_seccion || 0), 0) / totalEncuestas;
    const totalPacientes = encuestasData.filter(e => e.rol_usuario === 'paciente').length;
    const totalTerapeutas = encuestasData.filter(e => e.rol_usuario === 'terapeuta').length;

    document.getElementById('total-encuestas').textContent = totalEncuestas;
    document.getElementById('promedio-general').textContent = promedioGeneral.toFixed(2);
    document.getElementById('total-pacientes').textContent = totalPacientes;
    document.getElementById('total-terapeutas').textContent = totalTerapeutas;
}

// Actualizar tabla
function actualizarTabla() {
    const tbody = document.getElementById('tbody-encuestas');
    tbody.innerHTML = '';

    encuestasData.forEach(encuesta => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${encuesta.id}</td>
            <td>Usuario ${encuesta.usuario_id}</td>
            <td>${encuesta.rol_usuario}</td>
            <td>${new Date(encuesta.fecha_encuesta).toLocaleDateString()}</td>
            <td>${encuesta.puntuacion_total || 0}</td>
            <td>${(encuesta.promedio_seccion || 0).toFixed(2)}</td>
            <td>
                <button class="btn-small btn-view" onclick="verDetalles(${encuesta.id})">👁️ Ver</button>
                <button class="btn-small btn-export" onclick="exportarEncuesta(${encuesta.id})">📥 Exportar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Inicializar gráficos
function inicializarGraficos() {
    crearGraficoSecciones();
    crearGraficoRoles();
    crearGraficoEvolucion();
    crearGraficoPreguntas();
}

// Gráfico de puntuación por sección
function crearGraficoSecciones() {
    const ctx = document.getElementById('chart-secciones').getContext('2d');
    
    const secciones = [
        'Facilidad de Uso', 'Eficiencia', 'Atracción', 
        'Inclusivo', 'Evitar Frustración', 'Satisfacción General'
    ];
    
    const promedios = secciones.map((_, index) => {
        const startIdx = index * 4 + 1;
        const preguntas = encuestasData.flatMap(encuesta => 
            [1,2,3,4].map(i => encuesta[`q${startIdx + i - 1}`]).filter(v => v)
        );
        return preguntas.length ? preguntas.reduce((a, b) => a + b) / preguntas.length : 0;
    });

    charts.secciones = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: secciones,
            datasets: [{
                label: 'Puntuación Promedio',
                data: promedios,
                backgroundColor: '#5f9ea0',
                borderColor: '#4a8a8d',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

// Gráfico de distribución por roles
function crearGraficoRoles() {
    const ctx = document.getElementById('chart-roles').getContext('2d');
    
    const pacientes = encuestasData.filter(e => e.rol_usuario === 'paciente').length;
    const terapeutas = encuestasData.filter(e => e.rol_usuario === 'terapeuta').length;

    charts.roles = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pacientes', 'Terapeutas'],
            datasets: [{
                data: [pacientes, terapeutas],
                backgroundColor: ['#3498db', '#e74c3c'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Gráfico de evolución temporal
function crearGraficoEvolucion() {
    const ctx = document.getElementById('chart-evolucion').getContext('2d');
    
    // Agrupar por mes
    const datosPorMes = {};
    encuestasData.forEach(encuesta => {
        const fecha = new Date(encuesta.fecha_encuesta);
        const mes = `${fecha.getFullYear()}-${fecha.getMonth() + 1}`;
        if (!datosPorMes[mes]) {
            datosPorMes[mes] = [];
        }
        datosPorMes[mes].push(encuesta.promedio_seccion || 0);
    });

    const labels = Object.keys(datosPorMes).sort();
    const promedios = labels.map(mes => {
        const valores = datosPorMes[mes];
        return valores.reduce((a, b) => a + b) / valores.length;
    });

    charts.evolucion = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Puntuación Promedio Mensual',
                data: promedios,
                borderColor: '#9b59b6',
                backgroundColor: 'rgba(155, 89, 182, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

// Gráfico de preguntas mejor/peor valoradas
function crearGraficoPreguntas() {
    const ctx = document.getElementById('chart-preguntas').getContext('2d');
    
    const promediosPreguntas = [];
    for (let i = 1; i <= 24; i++) {
        const valores = encuestasData.map(e => e[`q${i}`]).filter(v => v !== undefined && v !== null);
        const promedio = valores.length ? valores.reduce((a, b) => a + b) / valores.length : 0;
        promediosPreguntas.push({
            pregunta: i,
            promedio: promedio
        });
    }

    // Ordenar y tomar las 5 mejores y peores
    promediosPreguntas.sort((a, b) => b.promedio - a.promedio);
    const mejores = promediosPreguntas.slice(0, 5);
    const peores = promediosPreguntas.slice(-5).reverse();

    charts.preguntas = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                ...mejores.map(m => `P${m.pregunta}`),
                ...peores.map(p => `P${p.pregunta}`)
            ],
            datasets: [
                {
                    label: 'Mejor Valoradas',
                    data: [...mejores.map(m => m.promedio), ...Array(5).fill(null)],
                    backgroundColor: '#27ae60'
                },
                {
                    label: 'Peor Valoradas',
                    data: [...Array(5).fill(null), ...peores.map(p => p.promedio)],
                    backgroundColor: '#e74c3c'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

// Ver detalles de encuesta
async function verDetalles(encuestaId) {
    try {
        const response = await fetch(VERENCUESTAID_URL.replace("1", encuestaId));
        const data = await response.json();
        
        if (data.success) {
            mostrarModalDetalles(data.encuesta);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los detalles de la encuesta');
    }
}

// Mostrar modal con detalles
function mostrarModalDetalles(encuesta) {
    const modalBody = document.getElementById('modal-detalles-body');
    
    let html = `
        <div class="detalles-encuesta">
            <div class="detalle-header">
                <h3>Encuesta #${encuesta.id}</h3>
                <p><strong>Usuario:</strong> ${encuesta.usuario_id} | <strong>Rol:</strong> ${encuesta.rol_usuario} | <strong>Fecha:</strong> ${new Date(encuesta.fecha_encuesta).toLocaleString()}</p>
            </div>
            
            <div class="secciones-grid">
    `;

    // Secciones de la encuesta
    const secciones = [
        { titulo: 'Facilidad de Uso', preguntas: [1,2,3,4] },
        { titulo: 'Eficiencia', preguntas: [5,6,7,8] },
        { titulo: 'Atracción', preguntas: [9,10,11,12] },
        { titulo: 'Inclusivo', preguntas: [13,14,15,16] },
        { titulo: 'Evitar Frustración', preguntas: [17,18,19,20] },
        { titulo: 'Satisfacción General', preguntas: [21,22,23,24] }
    ];

    secciones.forEach(seccion => {
        html += `
            <div class="seccion-detalle">
                <h4>${seccion.titulo}</h4>
                <div class="preguntas-list">
        `;
        
        seccion.preguntas.forEach(pregunta => {
            const valor = encuesta[`P${pregunta}`];
            html += `
                <div class="pregunta-item">
                    <span class="pregunta-text">P${pregunta}:</span>
                    <span class="pregunta-valor ${valor >= 4 ? 'alta' : valor <= 2 ? 'baja' : 'media'}">
                        ${valor || 'No respondida'}
                    </span>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });

    // Preguntas abiertas
    if (encuesta.que_mas_gusto || encuesta.que_mejorar || encuesta.que_confuso_frustrante) {
        html += `
            <div class="seccion-detalle full-width">
                <h4>Comentarios Abiertos</h4>
                <div class="comentarios-list">
        `;
        
        if (encuesta.que_mas_gusto) {
            html += `
                <div class="comentario-item">
                    <strong>¿Qué fue lo que más te gustó?</strong>
                    <p>${encuesta.que_mas_gusto}</p>
                </div>
            `;
        }
        
        if (encuesta.que_mejorar) {
            html += `
                <div class="comentario-item">
                    <strong>¿Qué aspecto se podría mejorar?</strong>
                    <p>${encuesta.que_mejorar}</p>
                </div>
            `;
        }
        
        if (encuesta.que_confuso_frustrante) {
            html += `
                <div class="comentario-item">
                    <strong>¿Hubo algo confuso o frustrante?</strong>
                    <p>${encuesta.que_confuso_frustrante}</p>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
    }

    html += `
            </div>
        </div>
    `;

    modalBody.innerHTML = html;
    document.getElementById('modal-detalles').style.display = 'block';
}

// Exportar datos
async function exportarDatos() {
    try {
        const response = await fetch(VERENCUESTA_URL);
        const blob = await response.blob();
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `encuestas_usabilidad_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error al exportar:', error);
        alert('Error al exportar los datos');
    }
}

     

// Exportar encuesta individual
async function exportarEncuesta(encuestaId) {
    try {
        const response = await fetch(`/api/encuestas/${encuestaId}/export`);
        const blob = await response.blob();
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `encuesta_${encuestaId}_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error al exportar encuesta:', error);
        alert('Error al exportar la encuesta');
    }
}

// Filtros
function inicializarFiltros() {
    document.getElementById('filtro-rol').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-fecha').addEventListener('change', aplicarFiltros);
}

function aplicarFiltros() {
    const rol = document.getElementById('filtro-rol').value;
    const fecha = document.getElementById('filtro-fecha').value;
    
    
}

// Utilidades
function cerrarModal() {
    document.getElementById('modal-detalles').style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('modal-detalles');
    if (event.target === modal) {
        cerrarModal();
    }
}
