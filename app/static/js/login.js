
let deferredPrompt;

// Registrar el Service Worker primero
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js", { scope: '/' })
    .then(() => console.log("Service Worker registrado"))
    .catch(err => console.log("Error SW:", err));
}

// Escuchar beforeinstallprompt laza el evento si la aplicacion cumple los requisitos
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // Evita el prompt automatico
    deferredPrompt = e;
    createInstallButton();
});
//boton que va a desencadenar el enveto para pwa
function createInstallButton() {
    if (!document.getElementById('install-btn')) {
        const installBtn = document.createElement('button');
        installBtn.id = 'install-btn';
        installBtn.textContent = "Instalar App";
        installBtn.classList.add("install-btn");
        document.body.appendChild(installBtn);
          //cuando se presiona el btn mouestra el prompt de instlacion
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;//esto hace que sepa si el usuario acepto o rechazo
               
                //limpia el evento para evitar ser reutilizado
                deferredPrompt = null;
                window.location.reload();
            }
        });
       
    }
}
document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('password');
    const isPassword = passwordInput.type === 'password';
    passwordInput.type = isPassword ? 'text' : 'password';
    
   
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});