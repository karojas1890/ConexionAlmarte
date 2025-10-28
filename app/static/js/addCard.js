let stream = null;

// Detecta si es dispositivo móvil
function isMobileDevice() {
    const userAgent = navigator.userAgent.toLowerCase();
    const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent);
    const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    const isSmallScreen = window.innerWidth <= 768;

    return isMobile || (hasTouch && isSmallScreen);
}

// Mostrar/ocultar botón escaneo según dispositivo
window.addEventListener('DOMContentLoaded', function() {
    const scanButton = document.querySelector('.btn-scan-card');
    if (!isMobileDevice()) {
        scanButton.style.display = 'none';
    } else {
        scanButton.style.display = 'flex';
    }
});

// Abrir cámara
async function openScanner() {
    const modal = document.getElementById('scannerModal');
    const video = document.getElementById('cameraVideo');

    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { exact: 'environment' }, width: { ideal: 1920 }, height: { ideal: 1080 } }
        });
        video.srcObject = stream;
        modal.classList.add('active');
    } catch (error) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } }
            });
            video.srcObject = stream;
            modal.classList.add('active');
        } catch {
            
              showModal('No se pudo acceder a la cámara.', 'Ingresa los datos manualmente.','"error"');
        }
    }
}

// Cerrar cámara y modal
function closeScanner() {
    const modal = document.getElementById('scannerModal');
    const video = document.getElementById('cameraVideo');

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    video.srcObject = null;
    modal.classList.remove('active');
}

// Capturar tarjeta y rellenar inputs
async function captureCard() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('captureCanvas');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const ctx = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        loadingOverlay.classList.add('active');

        try {
            const formData = new FormData();
            formData.append('card_image', blob, 'card.jpg');

            const response = await fetch(SCANCARD_URL, { method: 'POST', body: formData });
            const data = await response.json();

            if (data.success) {
                if (data.cardNumber) document.getElementById('cardNumber').value = data.cardNumber;
                if (data.cardHolder) document.getElementById('cardHolder').value = data.cardHolder;
                if (data.expiryDate) document.getElementById('expiryDate').value = data.expiryDate;

                updatePreview();
                closeScanner();
             
                 showModal('Datos de la tarjeta detectados', 'Revisa y presiona "Guardar Tarjeta','success');
            } else {
               
                  showModal('No se pudo leer la tarjeta', 'Ingresa los datos manualmente.','error');
            }
        } catch {
          
            showModal('Error procesando la imagen', 'Ingresa los datos manualmente. ');
        } finally {
            loadingOverlay.classList.remove('active');
        }
    }, 'image/jpeg', 0.95);
}

// Formato número de tarjeta
function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '').replace(/[^0-9]/g, '');
    input.value = value.match(/.{1,4}/g)?.join(' ') || value;

    const firstDigit = value.charAt(0);
    const cardIcon = document.getElementById('cardIcon');
    cardIcon.textContent = '💳';
}

// Formato fecha expiración
function formatExpiry(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 2) value = value.slice(0, 2) + '/' + value.slice(2, 4);
    input.value = value;
}

// Actualizar preview tarjeta
function updatePreview() {
    document.getElementById('previewNumber').textContent = document.getElementById('cardNumber').value || '•••• •••• •••• ••••';
    document.getElementById('previewHolder').textContent = document.getElementById('cardHolder').value || 'NOMBRE COMPLETO';
    document.getElementById('previewExpiry').textContent = document.getElementById('expiryDate').value || 'MM/AA';
}

// Guardar tarjeta (submit)
async function handleSubmit(event) {
    event.preventDefault();

    const formData = {
        cardNumber: document.getElementById('cardNumber').value,
        cardHolder: document.getElementById('cardHolder').value,
        expiryDate: document.getElementById('expiryDate').value,
        cvv: document.getElementById('cvv').value,
        setDefault: document.getElementById('setDefault').checked
    };

    try {
        const response = await fetch(ADDCARD_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            
            showModal('Tarjeta agregada exitosamente', data.message,'success');
            document.getElementById('cardForm').reset();
            updatePreview();
        } else {
      

             showModal('Error al guardar la tarjeta:', data.message,'error');
        }
    } catch (error) {
        
        showModal('Error al guardar la tarjeta:', 'Intente Nuevamente.','error');
    }
}



function deleteCard(cardId) {
    
         showModal('Tarjeta eliminada:', 'Esta tarjeta fue eliminada.','success');
    
}



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

        // Si es predeterminada, agregamos una clase especial
        if (card.predeterminada) cardDiv.classList.add("card-default-active");

        cardDiv.innerHTML = `
            <div class="card-header">
                <span class="card-type">${card.tipo || "Tarjeta"}</span>
                ${card.predeterminada ? `<span class="card-default">Predeterminada</span>` : ""}
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
                <button class="btn-card-action" onclick="setDefaultCard(${card.id_tarjeta})">
                    ${card.predeterminada ? "Predeterminada" : "Hacer predeterminada"}
                </button>
                <button class="btn-card-action" onclick="deleteCard(${card.id_tarjeta})">Eliminar</button>
            </div>
        `;

        container.appendChild(cardDiv);
    });
}
