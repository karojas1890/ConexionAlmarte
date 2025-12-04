
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

        function openBiometricModal() {
            document.getElementById('biometricModal').classList.add('active');
            simulateBiometricAuth();
        }

        function closeBiometricModal() {
            document.getElementById('biometricModal').classList.remove('active');
            document.getElementById('biometricError').classList.remove('show');
            document.getElementById('biometricContent').style.display = 'block';
            document.getElementById('biometricLoading').style.display = 'none';
        }

     async function simulateBiometricAuth() {
    document.getElementById('biometricContent').style.display = 'none';
    document.getElementById('biometricLoading').style.display = 'block';
    document.getElementById('biometricError').classList.remove('show');

    try {
        // 1. Obtener el challenge del backend (obligatorio)
        const publicKey = await fetch('/webauthn/login-challenge').then(r => r.json());

        // 2. Solicitar autenticación biométrica al dispositivo
        const assertion = await navigator.credentials.get({
            publicKey: publicKey
        });

        // 3. Enviar la respuesta al backend para verificar
        const response = await fetch('/webauthn/login-verify', {
            method: 'POST',
            body: JSON.stringify(assertion),
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();

        // 4. Resultado final de autenticación
        if (result.success) {
            window.location.href = '/dashboard';
        } else {
            showBiometricError("No se pudo autenticar con huella.");
        }

    } catch (err) {
        console.error(err);
        showBiometricError("Error: el dispositivo no pudo autenticar por biométricos.");
    }
}

function showBiometricError(msg) {
    document.getElementById('biometricLoading').style.display = 'none';
    document.getElementById('biometricContent').style.display = 'block';

    const errorDiv = document.getElementById('biometricError');
    errorDiv.textContent = msg;
    errorDiv.classList.add('show');
}
