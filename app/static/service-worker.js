const CACHE_NAME = "flask-pwa-v7";//se actualiza la version
const urlsToCache = [
  "/",                              // Pagina principal
  "/static/css/loginStyle.css",        // CSS         
  "/static/images/fondo.png",    // Imagen principal
  "/static/images/logo.png"         // Logo
];

// Instalación del service worker y cache inicial
self.addEventListener("install", (event) => {
  console.log("[ServiceWorker] Install");
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log("[ServiceWorker] Caching files");
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting(); // Activa inmediatamente
});

// Activación del service worker y limpieza de caches antiguas
self.addEventListener("activate", (event) => {
  console.log("[ServiceWorker] Activate");
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim(); // Toma control de los clientes inmediatamente
});

// Interceptar requests y servir desde cache si está disponible
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response; // Devuelve cache
        }
        // Si no está en cache, hace fetch normal
        return fetch(event.request).catch(() => {
          // Opcional: respuesta fallback si no hay internet
          if (event.request.destination === "document") {
            return caches.match("/");
          }
        });
      })
  );
});
