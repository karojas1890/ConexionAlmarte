document.addEventListener("DOMContentLoaded", async () => {
    const container = document.querySelector(".content");

  
    const estados = {
        1: "Muy Bajo",
        2: "Bajo",
        3: "Medio",
        4: "Alto",
        5: "Muy Alto"
    };

    try {
      
        const response = await fetch(`/tools/HistorialHerramientas`);
        if (!response.ok) throw new Error("Error al obtener los registros.");

        const registros = await response.json();

        if (!registros || registros.length === 0) {
            container.innerHTML = `
                <div class="page-title">Progreso en uso de estrategia de salud mental</div>
                <p>No se encontraron registros aún.</p>
            `;
            return;
        }

     
        container.innerHTML = `
            <div class="page-title">Progreso en uso de estrategia de salud mental</div>
        `;

        
        registros.forEach(r => {
            const card = document.createElement("div");
            card.classList.add("progress-card");

            card.innerHTML = `
                <div class="progress-header">${r.nombrerecomendacion || 'Sin nombre'}</div>
                <div class="progress-category">Categoría: ${r.nombrecategoria || 'Sin categoría'}</div>

                <div class="progress-metrics">
                    <div class="metric-box">
                        <div class="metric-label">Estado de Ánimo</div>
                        <div class="metric-value">
                            <span class="status-badge">${estados[r.animoantes] || '—'}</span>
                            <span class="arrow">→</span>
                            <span class="status-badge">${estados[r.animodespues] || '—'}</span>
                        </div>
                    </div>

                    <div class="metric-box">
                        <div class="status-title">Nivel de Bienestar</div>
                        <div class="status-change">
                            <span class="status-badge">${estados[r.bienestarantes] || '—'}</span>
                            <span class="arrow">→</span>
                            <span class="status-badge">${estados[r.bienestardespues] || '—'}</span>
                        </div>
                    </div>
                </div>

                <div class="progress-observation">
                    <div class="observation-label">Observación</div>
                    <div class="observation-text">${r.comentario || 'Sin observación'}</div>
                </div>

              
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        container.innerHTML = `<p style="color:red;">Error al cargar los datos del progreso.</p>`;
    }
});