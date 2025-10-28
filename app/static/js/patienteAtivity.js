function toggleDetails(element) {
            element.classList.toggle('expanded');
        }

        function filterActivities() {
            const activityType = document.getElementById('activityType').value;
            const dateFrom = document.getElementById('dateFrom').value;
            const dateTo = document.getElementById('dateTo').value;
            const status = document.getElementById('statusFilter').value;

            console.log('Filtros aplicados:', {
                activityType,
                dateFrom,
                dateTo,
                status
            });

            // Aquí implementarías la lógica de filtrado con el backend
            alert('Filtros aplicados. Aquí se cargarían los resultados filtrados desde el backend.');
        }

        function previousPage() {
            console.log('Página anterior');
            // Implementar lógica de paginación
        }

        function nextPage() {
            console.log('Página siguiente');
            // Implementar lógica de paginación
        }