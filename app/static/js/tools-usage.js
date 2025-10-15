  // Slider functionality
        const slider = document.getElementById('effectiveness');
        slider.addEventListener('input', function() {
            const value = (this.value - this.min) / (this.max - this.min) * 100;
            this.style.background = `linear-gradient(to right, #7FA8A3 0%, #7FA8A3 ${value}%, #ddd ${value}%, #ddd 100%)`;
        });

        // Mood selector functionality
        function setupMoodSelector(containerId) {
            const container = document.getElementById(containerId);
            const options = container.querySelectorAll('.mood-option');
            
            options.forEach(option => {
                option.addEventListener('click', function() {
                    options.forEach(opt => opt.classList.remove('selected'));
                    this.classList.add('selected');
                });
            });
        }

        setupMoodSelector('moodBefore');
        setupMoodSelector('moodAfter');
        setupMoodSelector('wellnessBefore');

        // Form submission
        document.getElementById('usageForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Uso de estrategia guardado exitosamente');
            window.location.href = 'tools-progress.html';
        });