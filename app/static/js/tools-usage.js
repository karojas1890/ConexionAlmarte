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


     document.addEventListener("DOMContentLoaded", () => {
    const guardarBtn = document.getElementById("guardarUsoBtn");
    const moodBeforeOptions = document.querySelectorAll("#moodBefore .mood-option");
    const moodAfterOptions = document.querySelectorAll("#moodAfter .mood-option");
    const wellnessBeforeOptions = document.querySelectorAll("#wellnessBefore .mood-option");
    const wellnessAfterOptions = document.querySelectorAll("#wellnessAfter .mood-option");
    const effectivenessSlider = document.getElementById("effectiveness");
    const strategy = parseInt(localStorage.getItem("idasignacionSeleccionada"));

    const observations = document.getElementById("observations");
    alert(strategy)
    const moodMap = { "muy-mal": 1, "regular": 2, "bien": 3, "muy-bien": 4 };
    const wellnessMap = { "muy-bajo": 1, "bajo": 2, "medio": 3, "alto": 4, "muy-alto": 5 };

    const getMoodValue = (options, map) => {
        for (let opt of options) {
            if (opt.classList.contains("selected")) return map[opt.dataset.value];
        }
        return null;
    };

    const setupMoodSelector = (options) => {
        options.forEach(opt => {
            opt.addEventListener("click", () => {
                options.forEach(o => o.classList.remove("selected"));
                opt.classList.add("selected");
            });
        });
    };

    setupMoodSelector(moodBeforeOptions);
    setupMoodSelector(moodAfterOptions);
    setupMoodSelector(wellnessBeforeOptions);
    setupMoodSelector(wellnessAfterOptions);

    guardarBtn.addEventListener("click", async () => {
        const data = {
            idasignacion: strategy,
            efectividad: parseInt(effectivenessSlider.value),
            animoAntes: getMoodValue(moodBeforeOptions, moodMap),
            animoDespues: getMoodValue(moodAfterOptions, moodMap),
            bienestarAntes: getMoodValue(wellnessBeforeOptions, wellnessMap),
            bienestarDespues: getMoodValue(wellnessAfterOptions, wellnessMap),
            comentario: observations.value
        };

        try {
            const res = await fetch('/tools/GuardarUso', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const resp = await res.json();

            if (resp.success) {
                alert("Uso registrado correctamente!");
                document.getElementById("usageForm").reset();
                document.querySelectorAll(".mood-option.selected").forEach(opt => opt.classList.remove("selected"));
            } else {
                alert("Error: " + resp.error);
            }
        } catch (err) {
            console.error("Error al registrar uso:", err);
        }
    });
});