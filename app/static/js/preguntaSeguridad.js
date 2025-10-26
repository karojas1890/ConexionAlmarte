  
        const securityQuestions = [
           
            {
                id: 'id_digits',
                label: 'Indique los últimos 4 dígitos de su número de identificación',
                type: 'text',
                placeholder: 'Ej: 123',
                maxlength: 3,
                pattern: '[0-9]{4}'
            },
           
        ];

        // Seleccionar 2 preguntas aleatorias
        function getRandomQuestions() {
            const shuffled = [...securityQuestions].sort(() => 0.5 - Math.random());
            return shuffled.slice(0, 2);
        }

        // Inicializar preguntas
        const selectedQuestions = getRandomQuestions();
        
        // Configurar pregunta 1
        const q1 = selectedQuestions[0];
        document.getElementById('question1Label').textContent = q1.label;
        const input1 = document.getElementById('question1');
        input1.type = q1.type;
        input1.placeholder = q1.placeholder || '';
        if (q1.maxlength) input1.maxLength = q1.maxlength;
        if (q1.pattern) input1.pattern = q1.pattern;

        

        // Manejar envío del formulario
        document.getElementById('securityForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const answer1 = document.getElementById('question1').value;
            

            
            validateSecurityAnswers(answer1, answer2, q1.id, q2.id);
        });

        function validateSecurityAnswers(answer1, answer2, questionId1, questionId2) {
         
            
            fetch('/api/validate-security-questions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question1: questionId1,
                    answer1: answer1,
                    question2: questionId2,
                    answer2: answer2
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Respuestas correctas
                    document.getElementById('successMessage').classList.add('show');
                    document.getElementById('errorMessage').classList.remove('show');
                    
                    // Enviar código por correo (esto se hace en el backend)
                    // Redirigir después de 3 segundos
                    setTimeout(() => {
                        window.location.href = 'reset-password.html';
                    }, 3000);
                } else {
                    // Respuestas incorrectas
                    document.getElementById('errorMessage').classList.add('show');
                    document.getElementById('successMessage').classList.remove('show');
                    
                    // Deshabilitar el formulario
                    document.getElementById('securityForm').style.opacity = '0.5';
                    document.getElementById('securityForm').style.pointerEvents = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al validar las respuestas. Por favor, intenta nuevamente.');
            });
        }