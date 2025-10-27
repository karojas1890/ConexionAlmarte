  
        const securityQuestions = [
           
            {
                id: 'id_digits',
                label: 'Indique los últimos 3 dígitos de su número de identificación',
                type: 'text',
                placeholder: 'Ej: 123',
                maxlength: 4,
                pattern: '[0-9]{3}'
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
            

            
            validateSecurityAnswers(answer1, q1.id);
        });

        function validateSecurityAnswers(answer1,  questionId1) {
         
            
            fetch(Questions_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question1: questionId1,
                    answer1: answer1,
                    
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