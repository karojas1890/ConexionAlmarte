 function openToolDetail() {
           window.location.href = '/routes/tools_details';
        }
        document.addEventListener("DOMContentLoaded", async () => {
    // Obtener id de asignación desde localStorage
    const idAsignacion = localStorage.getItem("idasignacionSeleccionada");
    if (!idAsignacion) {
        console.warn("No hay id de asignación en localStorage");
        return;
    }

    try {
        // Llamar al endpoint Flask
        const res = await fetch(`/tools/Recomendacion/${idAsignacion}`);
        if (!res.ok) throw new Error("No se pudo cargar la recomendación");

        const data = await res.json();

        // Seleccionar la card y rellenarla con innerHTML
        const card = document.getElementById("tool-card");
        card.innerHTML = `
            <div class="section-titleTools" id="tool-title">${data.nombreRecomendacion}</div>
            <div class="section-subtitleTools" id="tool-category">Categoría: ${data.categoria}</div>
            <div class="tool-image" id="tool-image" style="background-image: ${data.urlimagen ? `url(/static/images/${data.urlimagen})` : ''};"></div>
            <div class="tool-description" id="tool-description">${data.descripcion}</div>
            <div class="tool-actions">
                <a style="text-decoration: none;" href="{{ url_for('routes.tools_details') }}" class="btn-primary">Entendido</a>
                <button class="btn-primary" style="background: #4CAF50;">Obtener ayuda de IA</button>
            </div>
        `;

    } catch (error) {
        console.error("Error cargando recomendación:", error);
        const card = document.getElementById("tool-card");
        card.innerHTML = `<div class="tool-description">Error al cargar la recomendación.</div>`;
    }
});