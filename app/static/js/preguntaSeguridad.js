
const securityQuestions = [
    {
        id: 'id_digits',
        label: 'Indique los últimos 3 dígitos de su número de identificación',
        type: 'text',
        placeholder: 'Ej: 123',
        maxlength: 4,
        pattern: '[0-9]{3}'
    },
    {
        id: 'birthdate',
        label: 'Seleccione su fecha de nacimiento',
        type: 'date',
        placeholder: ''
    },
    {
        id: 'canton',
        label: 'Indique su Cantón',
        type: 'text',
        placeholder: ''
    },
    {
        id: 'phone_digits',
        label: 'Indique los últimos 3 dígitos de su número de teléfono',
        type: 'tel',
        placeholder: 'Ej: 123',
        maxlength: 3,
        pattern: '[0-9]{3}'
    }
];
const securityQuestionsTerapeuta = [
    {
        id: 'id_digits',
        label: 'Indique los últimos 3 dígitos de su número de identificación',
        type: 'text',
        placeholder: 'Ej: 123',
        maxlength: 4,
        pattern: '[0-9]{3}'
    },
    {
        id: 'M_last_name',
        label: 'Indique su segundo Apellido',
        type: 'text',
        placeholder: ''
    },
   
    {
        id: 'code',
        label: 'Indique los últimos 3 de su codigo profesional',
        type: 'text',
        placeholder: 'Ej: 123',
        maxlength: 3,
        pattern: '[0-9]{3}'
    }
];
const tipoUsuario = localStorage.getItem('tipoUsuario');

let preguntasActivas;
if (tipoUsuario === '2') {
    preguntasActivas = securityQuestionsTerapeuta;
} else if(tipoUsuario === '1') {
    preguntasActivas = securityQuestions;
}
// --- Obtener una pregunta aleatoria evitando repetir la última ---
function getRandomQuestion() {
    const lastUsed = sessionStorage.getItem('lastQuestion');

    if (!preguntasActivas || preguntasActivas.length === 0) {
        console.error("⚠️ No hay preguntas disponibles.");
        return null;
    }

    // Filtrar para evitar repetir la última pregunta usada
    let available = preguntasActivas.filter(q => q.id !== lastUsed);

    // Si solo hay una pregunta o el filtro la deja vacía, usar todas otra vez
    if (available.length === 0) {
        available = [...preguntasActivas];
    }

    // Elegir una pregunta aleatoria
    const randomQuestion = available[Math.floor(Math.random() * available.length)];

    // Guardar cuál fue la última mostrada
    sessionStorage.setItem('lastQuestion', randomQuestion.id);

    return randomQuestion;
}

// --- Inicializar ---
const q1 = getRandomQuestion();

if (q1) {
    // Asignar valores a los elementos del formulario
    document.getElementById('question1Label').textContent = q1.label;
    const input1 = document.getElementById('question1');
    input1.type = q1.type;
    input1.placeholder = q1.placeholder || '';
    if (q1.maxlength) input1.maxLength = q1.maxlength;
    if (q1.pattern) input1.pattern = q1.pattern;
} else {
    console.error("❌ No se pudo inicializar la pregunta de seguridad.");
}

// --- Envío del formulario ---
document.getElementById('securityForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const answer1 = document.getElementById('question1').value.trim();

    if (!answer1) {
        showModal('Alerta', 'Por favor, ingrese una respuesta.', 'error');
        return;
    }

    validateSecurityAnswers(answer1, q1.id,tipoUsuario);
});

function validateSecurityAnswers(answer1, questionId1,tipousuario) {
    fetch(Questions_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            question1: questionId1,
            answer1: answer1,
            tipouss:tipousuario,
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('successMessage').classList.add('show');
                document.getElementById('errorMessage').classList.remove('show');

                setTimeout(() => {
                    window.location.href = CODE_URL;
                }, 3000);
            } else {
                document.getElementById('errorMessage').textContent = data.message;
                document.getElementById('errorMessage').classList.add('show');
                document.getElementById('successMessage').classList.remove('show');

                if (data.blocked) {
                    document.getElementById('securityForm').style.opacity = '0.5';
                    document.getElementById('securityForm').style.pointerEvents = 'none';
                } else {
                    console.log(`Intentos fallidos: ${data.attempts}`);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al validar las respuestas. Por favor, intenta nuevamente.');
        });
}
