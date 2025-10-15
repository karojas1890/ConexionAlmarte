const slider = document.getElementById('effectiveness');
        slider.addEventListener('input', function() {
            const value = (this.value - this.min) / (this.max - this.min) * 100;
            this.style.background = `linear-gradient(to right, #7FA8A3 0%, #7FA8A3 ${value}%, #ddd ${value}%, #ddd 100%)`;
        });

        document.getElementById('progressForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Progreso guardado exitosamente');
            window.location.href = 'diary.html';
        });