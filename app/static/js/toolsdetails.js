
async function cargarHerramientas() {
    const container = document.getElementById("herramientas-container");
    container.innerHTML = ""; 

    const res = await fetch('/tools/recomendaciones_tools');
    const herramientas = await res.json();

    herramientas.forEach(r => {
        const card = document.createElement("div");
        card.className = "tool-detail-card";

        card.innerHTML = `
            <div class="tool-image">
                <img src="${r.urlimagen}" alt="${r.nombrerecomendacion}">
            </div>
            <div class="tool-title">${r.nombrerecomendacion}</div>
            <div class="tool-category">Categoría: ${r.nombrecategoria}</div>
            <div class="tool-description">${r.descripcion}</div>

            <div class="tool-meta">
                <div class="meta-item"><span>🕐</span><span>${r.momento}</span></div>
                <div class="meta-item"><span>📋</span><span>Cuándo se debe cumplir una tarea</span></div>
                <div class="meta-item"><span>📅</span><span>${r.duraciondias} días</span></div>
            </div>

            <div class="progress-section">
                <div class="progress-title">Progreso</div>
                <div class="progress-bar"><div class="progress-fill" style="width:0%;"></div></div>
                <div class="progress-text">0/${r.duraciondias}</div>
            </div>

            <div class="support-section">
                <div class="support-title">Enlaces de apoyo</div>
                <div class="support-item"><div class="support-text">Recurso 1</div><div class="support-arrow">›</div></div>
                <div class="support-item"><div class="support-text">Recurso 2</div><div class="support-arrow">›</div></div>
            </div>

             <div class="button-group">
                     <a class="btn btn-add" data-id="${r.idasignacion}" style="text-decoration: none;" href=${ROUTES.toolsMenu} >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 4V16M4 10H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
               Descripcion
            </a>
            <a class="btn btn-register" data-id="${r.idasignacion}" style="text-decoration: none;" href=${ROUTES.toolsUsage} >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M16 5L7.5 13.5L4 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Registrar uso
            </a>
            <a class="btn btn-progress" data-id="${r.idasignacion}" style="text-decoration: none;" href=${ROUTES.toolsProgress}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M3 10H17M10 3V17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="2" fill="none"/>
                </svg>
                Progreso
            </a>
                </div>
          
        `;

    card.querySelectorAll(".button-group a").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const id = btn.getAttribute("data-id");
                localStorage.setItem("idasignacionSeleccionada", id);
                console.log("Guardado en localStorage:", id);
            });
        });

        container.appendChild(card);
    });
}
document.addEventListener("DOMContentLoaded", function() {
    cargarHerramientas();
});