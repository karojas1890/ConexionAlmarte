// Objeto para almacenar todas las respuestas
const respuestasEncuesta = {
    // Preguntas de escala 1-5
    q1: null, q2: null, q3: null, q4: null, q5: null, q6: null, q7: null, q8: null,
    q9: null, q10: null, q11: null, q12: null, q13: null, q14: null, q15: null, q16: null,
    q17: null, q18: null, q19: null, q20: null, q21: null, q22: null, q23: null, q24: null,
    
    // Preguntas abiertas
    open1: '',
    open2: '',
    open3: ''
};

let currentSection = 'intro';

// Función para mostrar/ocultar secciones
function showSection(section) {
    // Guardar respuestas de la sección actual antes de cambiar
    guardarRespuestasSeccionActual();
    
    // Ocultar sección actual
    document.getElementById(`section-${currentSection}`).classList.remove('active');
    
    // Actualizar progreso
    updateProgress(section);
    
    // Mostrar nueva sección
    currentSection = section;
    document.getElementById(`section-${section}`).classList.add('active');
    
    // Restaurar respuestas guardadas en la nueva sección
    restaurarRespuestasSeccion(section);
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Función para actualizar la barra de progreso
function updateProgress(section) {
    // Reset all steps
    for (let i = 1; i <= 7; i++) {
        const step = document.getElementById(`step-${i}`);
        step.classList.remove('completed', 'active');
    }
    
    // Mark completed and active steps
    const sectionMap = {
        'intro': 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 6,
        6: 7,
        'open': 7
    };
    
    const currentStep = sectionMap[section];
    
    for (let i = 1; i < currentStep; i++) {
        document.getElementById(`step-${i}`).classList.add('completed');
    }
    
    document.getElementById(`step-${currentStep}`).classList.add('active');
}

// Función para guardar respuestas de escala
function guardarRespuesta(pregunta, valor) {
    respuestasEncuesta[pregunta] = valor;
    console.log(`Respuesta guardada: ${pregunta} = ${valor}`);
}

// Función para guardar respuestas de texto
function guardarRespuestaTexto(pregunta, texto) {
    respuestasEncuesta[pregunta] = texto;
    console.log(`Texto guardado: ${pregunta} = ${texto.substring(0, 50)}...`);
}

// Función para guardar todas las respuestas de la sección actual
function guardarRespuestasSeccionActual() {
    switch(currentSection) {
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
            // Las respuestas de escala ya se guardan automáticamente con los event listeners
            break;
        case 'open':
            // Guardar preguntas abiertas
            const open1 = document.querySelector('textarea[placeholder*="más te gustó"]');
            const open2 = document.querySelector('textarea[placeholder*="mejorar"]');
            const open3 = document.querySelector('textarea[placeholder*="confuso"]');
            
            if (open1) guardarRespuestaTexto('open1', open1.value);
            if (open2) guardarRespuestaTexto('open2', open2.value);
            if (open3) guardarRespuestaTexto('open3', open3.value);
            break;
    }
}

// Función para restaurar respuestas en una sección
function restaurarRespuestasSeccion(section) {
    switch(section) {
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
            // Restaurar respuestas de escala
            const sectionNum = parseInt(section);
            const startQuestion = (sectionNum - 1) * 4 + 1;
            
            for (let i = startQuestion; i < startQuestion + 4; i++) {
                const radio = document.querySelector(`input[name="q${i}"][value="${respuestasEncuesta[`q${i}`]}"]`);
                if (radio) {
                    radio.checked = true;
                }
            }
            break;
            
        case 'open':
            // Restaurar preguntas abiertas
            const open1 = document.querySelector('textarea[placeholder*="más te gustó"]');
            const open2 = document.querySelector('textarea[placeholder*="mejorar"]');
            const open3 = document.querySelector('textarea[placeholder*="confuso"]');
            
            if (open1) open1.value = respuestasEncuesta.open1 || '';
            if (open2) open2.value = respuestasEncuesta.open2 || '';
            if (open3) open3.value = respuestasEncuesta.open3 || '';
            break;
    }
}

// Función para validar que la encuesta esté completa
function validarEncuestaCompleta() {
    const preguntasFaltantes = [];
    
    // Verificar preguntas de escala
    for (let i = 1; i <= 24; i++) {
        if (respuestasEncuesta[`q${i}`] === null) {
            preguntasFaltantes.push(i);
        }
    }
    
    
    if (preguntasFaltantes.length > 0) {
        const primeraPregunta = preguntasFaltantes[0];
        if (typeof primeraPregunta === 'number') {
            // Es una pregunta de escala
            const seccion = Math.ceil(primeraPregunta / 4);
            showSection(seccion);
            alert(`Por favor, responde la pregunta ${primeraPregunta} en la sección ${seccion}`);
        } else {
            // Es una pregunta abierta
            showSection('open');
            alert(`Por favor, responde: ${primeraPregunta}`);
        }
        return false;
    }
    
    return true;
}

// Función para navegar hacia atrás
function goBack() {
    window.history.back();
}

// Función para mostrar modal de confirmación
function showConfirmationModal() {
    // Verificar que todas las respuestas estén completas
    if (!validarEncuestaCompleta()) {
        return;
    }
    document.getElementById('confirmationModal').style.display = 'flex';
}

// Función para ocultar modal de confirmación
function hideConfirmationModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

// Función para enviar encuesta al backend
async function submitSurvey() {
    try {
        // Cerrar el modal de confirmación inmediatamente
        hideConfirmationModal();
        
        // Mostrar loading
        showLoadingIndicator();
        
        const datosBackend = MapeoDatos(respuestasEncuesta);
        console.log('Enviando datos:', datosBackend);
        
        // Enviar al backend
        const resultado = await enviarEncuesta(datosBackend);
        
        // El éxito se maneja dentro de enviarEncuesta
        
    } catch (error) {
        console.error('Error al enviar encuesta:', error);
        hideLoadingIndicator();
        showModal('¡Error!', 'Error al enviar la encuesta. Por favor, intenta nuevamente.', 'error');
    }
}

function MapeoDatos(respuestasJS) {
    return {
        usuario_id: userId,
        rol_usuario: userRole,

        // Seccion 1
        navegacion_clara: respuestasJS.q1,
        facil_encontrar_funciones: respuestasJS.q2,
        instrucciones_claras: respuestasJS.q3,
        aprendizaje_rapido: respuestasJS.q4,

        // Seccion 2
        tareas_rapidas: respuestasJS.q5,
        pocos_pasos: respuestasJS.q6,
        proceso_citas_agil: respuestasJS.q7,
        registro_eficiente: respuestasJS.q8,

        // Seccion 3
        diseno_atractivo: respuestasJS.q9,
        colores_agradables: respuestasJS.q10,
        iconos_modernos: respuestasJS.q11,
        aspecto_general: respuestasJS.q12,

        // Seccion 4
        texto_comodo: respuestasJS.q13,
        contrastes_adecuados: respuestasJS.q14,
        diseno_inclusivo: respuestasJS.q15,
        lenguaje_respetuoso: respuestasJS.q16,

        // Sección 5
        proteccion_errores: respuestasJS.q17,
        mensajes_error_claros: respuestasJS.q18,
        respuesta_consistente: respuestasJS.q19,
        control_tranquilidad: respuestasJS.q20,

        // Seccinn 6
        satisfaccion_general: respuestasJS.q21,
        herramienta_util: respuestasJS.q22,            
        sentir_apoyado: respuestasJS.q23,              
        recomendaria_aplicacion: respuestasJS.q24,     

        // Comentarios Abiertos
        que_mas_gusto: respuestasJS.open1 || '',
        que_mejorar: respuestasJS.open2 || '',
        que_confuso_frustrante: respuestasJS.open3 || ''
    };
}

// Función para enviar datos al backend
async function enviarEncuesta(datosBackend) {
    try {
        const response = await fetch(URL_ENCUESTA, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(datosBackend)
        });

        const data = await response.json();
        console.log('Respuesta del backend:', data);

        // Verificar data.valido
        if (data.valido) {
            hideLoadingIndicator();
            showModal('¡Encuesta Registrada!', 'Gracias por completar la encuesta! Tus comentarios son muy valiosos para nosotros.', 'success');
            
            // Redirigir después de 2 segundos
            setTimeout(() => {
                window.location.href = DashBoard_URL;
            }, 2000);
            
            return data;
        } else {
            hideLoadingIndicator();
            showModal('¡Error!', 'No se pudo enviar la encuesta: ' + (data.error || data.mensaje || 'Error desconocido'), 'error');
            return null;
        }

    } catch (error) {
        console.error("Error de conexión:", error);
        showModal('¡Error!', 'Error de conexión. Por favor, verifica tu internet e intenta nuevamente.', 'error');
        return null;
    }
}

// Función para mostrar loading
function showLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-indicator';
    loadingDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        color: white;
        font-size: 18px;
    `;
    loadingDiv.innerHTML = `
        <div style="text-align: center;">
            <div style="border: 4px solid #f3f3f3; border-top: 4px solid #5f9ea0; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px;"></div>
            <p>Enviando encuesta...</p>
        </div>
    `;
    
    // Agregar estilo de animación
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(loadingDiv);
}

function hideLoadingIndicator() {
    const loading = document.getElementById('loading-indicator');
    if (loading) {
        loading.remove();
    }
}



// Inicializar event listeners cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Agregar event listeners a todos los radio buttons
    for (let i = 1; i <= 24; i++) {
        const radios = document.querySelectorAll(`input[name="q${i}"]`);
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                guardarRespuesta(`q${i}`, parseInt(this.value));
            });
        });
    }
    
    // Agregar event listeners a los textareas (debounce para mejor performance)
    const textareas = document.querySelectorAll('.open-question-input');
    textareas.forEach((textarea, index) => {
        let timeout;
        textarea.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                guardarRespuestaTexto(`open${index + 1}`, this.value);
            }, 300);
        });
    });
    
    // Inicializar progreso
    updateProgress('intro');
});

