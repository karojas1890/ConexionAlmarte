// Simulación de variable de sesión (en un caso real, esto vendría del servidor)
        // Para probar, cambia el valor a 'terapeuta' o 'paciente'
        const userRole = Rol;
      let currentSection = 'intro';
        
        function showSection(section) {
            // Ocultar sección actual
            document.getElementById(`section-${currentSection}`).classList.remove('active');
            
            // Actualizar progreso
            updateProgress(section);
            
            // Mostrar nueva sección
            currentSection = section;
            document.getElementById(`section-${section}`).classList.add('active');
            
            // Scroll to top
            window.scrollTo(0, 0);
        }
        
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
        
        function goBack() {
            window.history.back();
        }
        
        function showConfirmationModal() {
            document.getElementById('confirmationModal').style.display = 'flex';
        }
        
        function hideConfirmationModal() {
            document.getElementById('confirmationModal').style.display = 'none';
        }
        
        function submitSurvey() {
            // Aquí iría la lógica para enviar los datos al servidor
            hideConfirmationModal();
            
            // Simulación de envío exitoso
            setTimeout(() => {
                alert('¡Gracias por completar la encuesta! Tu feedback es muy valioso para nosotros.');
                window.location.href = DashBoard_URL;
            }, 500);
        }
        
        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            updateProgress('intro');
        });
        
        // Cerrar modal si se hace clic fuera de él
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('confirmationModal');
            if (event.target === modal) {
                hideConfirmationModal();
            }
        });