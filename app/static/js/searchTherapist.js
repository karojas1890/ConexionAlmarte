  // Elementos del DOM
        const codeInput = document.getElementById('almarte-code-input');
        const nameInput = document.getElementById('almarte-name-input');
        const searchBtn = document.getElementById('almarte-search-btn');
        const clearBtn = document.getElementById('almarte-clear-btn');
        const profileCard = document.getElementById('almarte-profile-card');
        const errorMessage = document.getElementById('almarte-error');
        const loading = document.getElementById('almarte-loading');
        const tabs = document.querySelectorAll('.almarte-search-tab');

        // Cambiar tabs
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                
                // Actualizar tabs activos
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Mostrar/ocultar inputs
                document.querySelectorAll('.almarte-search-tab-content').forEach(content => {
                    content.style.display = 'none';
                });
                document.getElementById(`tab-${tabName}`).style.display = 'block';

                // Limpiar errores
                errorMessage.classList.remove('show');
            });
        });

        // Función de búsqueda
        searchBtn.addEventListener('click', async () => {
            const isCodeTab = document.querySelector('.almarte-search-tab.active').getAttribute('data-tab') === 'code';
            const query = isCodeTab ? codeInput.value.trim() : nameInput.value.trim();

            if (!query) {
                showError('Por favor ingresa un valor para buscar');
                return;
            }

            await searchTherapist(query, isCodeTab);
        });

        // Función de limpiar
        clearBtn.addEventListener('click', () => {
            codeInput.value = '';
            nameInput.value = '';
            profileCard.classList.remove('active');
            errorMessage.classList.remove('show');
        });

        // Buscar profesional
      async function searchTherapist(query, isCode) {
    loading.classList.add('show');
    errorMessage.classList.remove('show');
    profileCard.classList.remove('active');

    try {
        const searchType = isCode ? 'code' : 'name';
        const response = await fetch(API_PSICOLOGOS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                searchType: searchType
            })
        });

        const data = await response.json();
        console.log(data);

        if (!response.ok || !data.resultado) {
            showError('No pudimos encontrar al profesional. Intenta de nuevo.');
            return;
        }

        displayTherapist(data.resultado);

    } catch (error) {
        showError('Ocurrió un error, intenta nuevamente.');
        console.error('Error:', error);
    } finally {
        loading.classList.remove('show');
    }
}

        // Mostrar perfil del profesional
        function displayTherapist(therapist) {
           document.getElementById('almarte-profile-image').src = therapist.imageUrl || `${IMAGE_URL}?height=150&width=150`;
           document.getElementById('almarte-profile-name').textContent = `${therapist.nombre} ${therapist.apellido1} ${therapist.apellido2 || ''}`.trim();
            document.getElementById('almarte-profile-code').textContent = `Código: ${therapist.codigoprofesional}`;

            // Estados
            const estadoTexts = {
                1: 'Activo',
                2: 'Inactivo',
                3: 'Suspendido'
            };
            const estadoClasses = {
                1: 'almarte-state-1',
                2: 'almarte-state-2',
                3: 'almarte-state-3'
            };

            const estadoBadge = document.getElementById('almarte-estado-badge');
            estadoBadge.textContent = `Estado: ${estadoTexts[therapist.estado] || 'Desconocido'}`;
            estadoBadge.className = `almarte-status-badge almarte-status-active ${estadoClasses[therapist.estado]}`;

            // Responsabilidad económica
            const economicBadge = document.getElementById('almarte-economic-badge');
            economicBadge.textContent = therapist.estadoresponsabilidadeconomica === 1 ? 'Responsabilidad: Sí' : 'Responsabilidad: No';

            // Área de trabajo
            document.getElementById('almarte-area-trabajo').textContent = therapist.areatrabajo || 'No disponible';

            // Habilitaciones
            document.getElementById('almarte-habilitaciones').textContent = therapist.habilitacionesevaluaciones || 'No disponible';

            profileCard.classList.add('active');
        }

        // Mostrar error
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.add('show');
        }

        // Enter para buscar
        [codeInput, nameInput].forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    searchBtn.click();
                }
            });
        });