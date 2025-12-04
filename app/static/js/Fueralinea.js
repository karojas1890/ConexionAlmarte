function showNetStatus(message, color) {
    const statusDiv = document.getElementById("net-status");
    statusDiv.textContent = message;
    statusDiv.style.background = color;
    statusDiv.style.display = "block";

    // Oculta el mensaje si vuelve conexion y dejo algo visible más de 1s
    setTimeout(() => {
        if (navigator.onLine) {
            statusDiv.style.display = "none";
        }
    }, 2000);
}

// Esto detecta cuando se pierde Internet
window.addEventListener("offline", () => {
    showNetStatus("Sin conexión a Internet", "#c0392b");
});

// Este cuando se recupera Internet
window.addEventListener("online", () => {
    showNetStatus("✅ Conexión restaurada", "#27ae60");
});

