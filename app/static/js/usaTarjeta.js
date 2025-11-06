
function renderCards(cards) {
    const container = document.getElementById("cardsContainer");
    container.innerHTML = ""; 

    if (!cards || cards.length === 0) {
        container.innerHTML = "<p style='text-align:center; color:#888;'>No tienes tarjetas registradas 🏦</p>";
        return;
    }

    cards.forEach(card => {
        const cardDiv = document.createElement("div");
        cardDiv.classList.add("card-item");

        cardDiv.innerHTML = `
            <div class="card-header">
                <span class="card-type">${card.tipo || "Tarjeta"}</span>
            </div>

            <div class="card-number">•••• •••• •••• ${card.ultimo4}</div>

            <div class="card-footer">
                <div class="card-holder">
                    <div style="font-size: 11px; opacity: 0.8;">TITULAR</div>
                    <div>${card.nombre_titular}</div>
                </div>
                <div class="card-expiry">
                    <div style="font-size: 11px; opacity: 0.8;">VENCE</div>
                    <div>${card.fecha_expiracion}</div>
                </div>
            </div>

            <div class="card-actions">
                <button class="btn-card-action" onclick='useCard(${JSON.stringify(card)})'>Usar esta tarjeta</button>             
            </div>
        `;

        container.appendChild(cardDiv);
    });
}



function useCard(card) {
    try {
        // Guarda la tarjeta seleccionada en localStorage
        localStorage.setItem("selectedCard", JSON.stringify(card));

        // Redirige a la vista del formulario de pago
        window.location.href = paymentforUrl; 
    } catch (error) {
        console.error("Error seleccionando tarjeta:", error);
        showModal('Error', 'No se pudo seleccionar la tarjeta.', 'error');
    }
}

async function loadUserCards() {
    try {
        const response = await fetch(GETCARD_URL);
        if (!response.ok) throw new Error("Error al cargar tarjetas");
        
        const cards = await response.json();
        renderCards(cards);  // Llama a la función que te di antes
    } catch (error) {
        console.error("Error cargando tarjetas:", error);
        const container = document.getElementById("cardsContainer");
        container.innerHTML = "<p style='text-align:center; color:#888;'>No se pudieron cargar las tarjetas</p>";
    }
}



window.addEventListener('DOMContentLoaded', loadUserCards);
