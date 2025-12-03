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
// Mapeo de nombres de columnas a textos de preguntas
    const mapeoPreguntas = {
        // Sección 1: Facilidad de Uso
        "P1": "La navegación dentro de la aplicación es clara y sencilla.",
        "P2": "Me resultó fácil encontrar las funciones que necesitaba.",
        "P3": "Las instrucciones y los textos son fáciles de entender.",
        "P4": "Aprender a usar la aplicación me tomó poco tiempo.",
        
        // Sección 2: Eficiencia
        "P5": "Puedo completar mis tareas de manera rápida",
        "P6": "La aplicación me permite lograr lo que necesito con pocos pasos.",
        "P7": "El proceso para programar o cancelar una cita es ágil y directo.",
        "P8": "El registro de mis disparadores y avances es un proceso eficiente.",
        
        // Sección 3: Atracción
        "P9": "El diseño de la aplicación es visualmente atractivo.",
        "P10": "La combinación de colores es agradable y transmite calma.",
        "P11": "Los iconos y botones son modernos y de buen gusto.",
        "P12": "Me gusta cómo se ve la aplicación en general.",
        
        // Sección 4: Inclusivo
        "P13": "El tamaño del texto es cómodo para leer.",
        "P14": "Los colores y contrastes utilizados no dificultan la lectura.",
        "P15": "El diseño considera diferentes necesidades de usuarios",
        "P16": "El lenguaje utilizado es respetuoso y no hace suposiciones sobre el usuario.",
        
        // Sección 5: Evitar Frustración
        "P17": "La aplicación me protege de cometer errores",
        "P18": "Si cometo un error, la aplicación me da un mensaje claro de cómo solucionarlo.",
        "P19": "La aplicación responde de forma consistente y predecible.",
        "P20": "Me sentí tranquilo/a y en control mientras usaba la aplicación.",
        
        // Sección 6: Satisfacción General
        "P21": "Estoy satisfecho/a con la experiencia general que tuve usando esta aplicación.",
        "P22": "La aplicación me parece una herramienta útil para gestionar mi bienestar mental.",
        "P23": "Recomendaría esta aplicación a otros colegas",
        "P24": "Me hace sentir apoyado en mis tareas diarias",

         "open1":"¿Qué fue lo que más te gustó de la aplicación?",
         "open2":"¿Qué aspecto de la aplicación crees que se podría mejorar?",
         "open3":"¿Hubo algo que te resultó confuso, frustrante o que no funcionó como esperabas?"
    };
function mostrarModalDetalles(encuesta) {
    const modalBody = document.getElementById('modal-detalles-body');
    
    

    let html = `
        <div class="detalles-encuesta">
            <div class="detalle-header">
                <h3>Encuesta #${encuesta.id}</h3>
                <p><strong>Usuario:</strong> ${encuesta.usuario_id} | <strong>Rol:</strong> ${encuesta.rol_usuario} | <strong>Fecha:</strong> ${new Date(encuesta.fecha_encuesta).toLocaleDateString()}</p>
            </div>
            
            <div class="secciones-grid">
    `;

    // Definir secciones con sus campos correspondientes
    const secciones = [
        {
            titulo: 'Facilidad de Uso',
            campos: ['P1', 'P2', 'P3', 'P4']
        },
        {
            titulo: 'Eficiencia',
            campos: ['P5', 'P6', 'P7', 'P8']
        },
        {
            titulo: 'Atracción',
            campos: ['P9', 'P10', 'P11', 'P12']
        },
        {
            titulo: 'Inclusivo',
            campos: ['P13', 'P14', 'P15', 'P16']
        },
        {
            titulo: 'Evitar Frustración',
            campos: ['P17', 'P18', 'P19', 'P20']
        },
        {
            titulo: 'Satisfacción General',
            campos: ['P21', 'P22', 'P23', 'P24']
        }
    ];

    secciones.forEach(seccion => {
        html += `
            <div class="seccion-detalle">
                <h4>${seccion.titulo}</h4>
                <div class="preguntas-list">
        `;
        
        seccion.campos.forEach((campo, index) => {
            const valor = encuesta[campo];
            const textoPregunta = mapeoPreguntas[campo];
            
            html += `
                <div class="pregunta-item">
                    <div class="pregunta-text">
                        <span class="pregunta-numero">${index + 1}.</span>
                        ${textoPregunta}
                    </div>
                    <div class="pregunta-respuesta">
                        <span class="pregunta-valor ${getClaseValor(valor)}">
                            ${valor !== null && valor !== undefined ? valor : 'No respondida'}
                        </span>
                        ${valor !== null && valor !== undefined ? '<span class="escala">/5</span>' : ''}
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    // Agregar preguntas abiertas si existen
    if (encuesta.open1 || encuesta.open3 || encuesta.open3) {
        html += `
            <div class="seccion-abiertas">
                <h4>Comentarios Adicionales</h4>
        `;
        
        if (encuesta.que_mas_gusto) {
            html += `
                <div class="comentario-item">
                    <h5>¿Qué fue lo que más le gustó de la aplicación?</h5>
                    <p class="comentario-texto">${encuesta.open1}</p>
                </div>
            `;
        }
        
        if (encuesta.que_mejorar) {
            html += `
                <div class="comentario-item">
                    <h5>¿Qué aspectos cree que podrían mejorar?</h5>
                    <p class="comentario-texto">${encuesta.open2}</p>
                </div>
            `;
        }
        
        if (encuesta.que_confuso_frustrante) {
            html += `
                <div class="comentario-item">
                    <h5>¿Qué le resultó confuso o frustrante?</h5>
                    <p class="comentario-texto">${encuesta.open3}</p>
                </div>
            `;
        }
        
        html += `</div>`;
    }
    
    // Resumen final
    html += `
            <div class="resumen-final">
                <div class="resumen-item">
                    <strong>Puntuación Total:</strong> ${encuesta.puntuacion_total || calcularTotal(encuesta)}
                </div>
                <div class="resumen-item">
                    <strong>Promedio General:</strong> ${encuesta.promedio_seccion || calcularPromedio(encuesta)}
                </div>
            </div>
        </div>
    `;
    
    modalBody.innerHTML = html;
    document.getElementById('modal-detalles').style.display = 'block';
}

// Función auxiliar para determinar clase CSS según valor
function getClaseValor(valor) {
    if (valor === null || valor === undefined) return 'no-respondida';
    if (valor >= 4) return 'alta';
    if (valor <= 2) return 'baja';
    return 'media';
}

// Función para calcular total si no viene del backend
function calcularTotal(encuesta) {
    let total = 0;
    const campos = Object.keys(mapeoPreguntas);
    
    campos.forEach(campo => {
        if (encuesta[campo] !== null && encuesta[campo] !== undefined) {
            total += parseInt(encuesta[campo]) || 0;
        }
    });
    
    return total;
}

// Función para calcular promedio si no viene del backend
function calcularPromedio(encuesta) {
    let total = 0;
    let contador = 0;
    const campos = Object.keys(mapeoPreguntas);
    
    campos.forEach(campo => {
        if (encuesta[campo] !== null && encuesta[campo] !== undefined) {
            total += parseInt(encuesta[campo]) || 0;
            contador++;
        }
    });
    
    return contador > 0 ? (total / contador).toFixed(2) : '0.00';
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

     


async function exportarEncuesta(encuesta) {
    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Configuración inicial
        const pageWidth = doc.internal.pageSize.width;
        const margin = 20;
        let yPos = 20;
        
        // Título
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        doc.text("Detalle de Encuesta", pageWidth / 2, yPos, { align: "center" });
        yPos += 15;
        
        // Información básica
        doc.setFontSize(11);
        doc.setFont("helvetica", "normal");
        doc.text(`ID: ${encuesta.usuario_id}`, margin, yPos);
        doc.text(`Usuario: ${encuesta.usuario_id}`, pageWidth / 2, yPos);
        yPos += 7;
        
        doc.text(`Rol: ${encuesta.rol_usuario}`, margin, yPos);
        doc.text(`Fecha: ${new Date(encuesta.fecha_encuesta).toLocaleDateString()}`, pageWidth / 2, yPos);
        yPos += 15;
        
        // Separador
        doc.setDrawColor(200, 200, 200);
        doc.line(margin, yPos, pageWidth - margin, yPos);
        yPos += 10;
        
        // Preguntas por secciones
        const secciones = [
            { titulo: 'Facilidad de Uso', preguntas: ['P1', 'P2', 'P3', 'P4'] },
            { titulo: 'Eficiencia', preguntas: ['P5', 'P6', 'P7', 'P8'] },
            { titulo: 'Atracción', preguntas: ['P9', 'P10', 'P11', 'P12'] },
            { titulo: 'Inclusivo', preguntas: ['P13', 'P14', 'P15', 'P16'] },
            { titulo: 'Evitar Frustración', preguntas: ['P17', 'P18', 'P19', 'P20'] },
            { titulo: 'Satisfacción General', preguntas: ['P21', 'P22', 'P23', 'P24'] }
        ];
        
        
        
        secciones.forEach(seccion => {
            // Verificar si se ocupa nueva pagina
            if (yPos > 250) {
                doc.addPage();
                yPos = 20;
            }
            
            // Título de seccion
            doc.setFontSize(14);
            doc.setFont("helvetica", "bold");
            doc.text(seccion.titulo, margin, yPos);
            yPos += 10;
            
            // Preguntas
            doc.setFontSize(10);
            doc.setFont("helvetica", "normal");
            
            seccion.preguntas.forEach((pregunta, index) => {
                const textoPregunta = mapeoPreguntas[pregunta];
                const respuesta = encuesta[pregunta];
                
                // Dividir texto largo
                const lines = doc.splitTextToSize(`${index + 1}. ${textoPregunta}`, pageWidth - 60);
                
                // Verificar espacio
                if (yPos + (lines.length * 5) + 10 > 280) {
                    doc.addPage();
                    yPos = 20;
                }
                
                doc.text(lines, margin + 5, yPos);
                yPos += lines.length * 5;
                
                // Respuesta
                doc.setFont("helvetica", "bold");
                doc.text(`Respuesta: ${respuesta || 'No respondida'} / 5`, margin + 10, yPos);
                yPos += 7;
                doc.setFont("helvetica", "normal");
                
                yPos += 3;  
            });
            
            yPos += 5;  
        });
        
        // Preguntas abiertas
        if (encuesta.open1 || encuesta.open2 || encuesta.open3) {
            if (yPos > 200) {
                doc.addPage();
                yPos = 20;
            }
            
            doc.setFontSize(14);
            doc.setFont("helvetica", "bold");
            doc.text("Comentarios Adicionales", margin, yPos);
            yPos += 10;
            
            doc.setFontSize(10);
            doc.setFont("helvetica", "normal");
            
            if (encuesta.open1) {
                const lines = doc.splitTextToSize(`• ${encuesta.open1}`, pageWidth - 40);
                doc.text(lines, margin, yPos);
                yPos += lines.length * 5 + 5;
            }
            
            if (encuesta.open2) {
                const lines = doc.splitTextToSize(`• ${encuesta.open2}`, pageWidth - 40);
                doc.text(lines, margin, yPos);
                yPos += lines.length * 5 + 5;
            }
            
            if (encuesta.open3) {
                const lines = doc.splitTextToSize(`• ${encuesta.open3}`, pageWidth - 40);
                doc.text(lines, margin, yPos);
                yPos += lines.length * 5 + 5;
            }
        }
        
       
        if (yPos > 250) {
            doc.addPage();
            yPos = 20;
        }
        
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.text("Resumen", margin, yPos);
        yPos += 10;
        
        doc.setFontSize(11);
        doc.setFont("helvetica", "normal");
        doc.text(`Puntuación Total: ${encuesta.puntuacion_total || calcularTotal(encuesta)}`, margin, yPos);
        yPos += 7;
        doc.text(`Promedio General: ${encuesta.promedio || calcularPromedio(encuesta)}`, margin, yPos);
        
         
        const totalPages = doc.internal.getNumberOfPages();
        for (let i = 1; i <= totalPages; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.text(
                `Página ${i} de ${totalPages} • Generado el ${new Date().toLocaleDateString()}`,
                pageWidth / 2,
                290,
                { align: "center" }
            );
        }
        
       
        doc.save(`encuesta_${encuesta.id}_${new Date().toISOString().split('T')[0]}.pdf`);
        
    } catch (error) {
        console.error('Error al generar PDF:', error);
        alert('Error al generar el PDF');
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
