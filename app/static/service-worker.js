const CACHE_NAME = "flask-pwa-v15"; 
const urlsToCache = [
  "/",
  "/static/css/loginStyle.css",
  "/static/images/fondo.png",
  "/static/images/logo.png"
];

// Instalar SW
self.addEventListener("install", (event) => {
  console.log("[ServiceWorker] Install");

  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[ServiceWorker] Caching safe files…");

      return Promise.all(
        urlsToCache.map((url) =>
          fetch(url)
            .then((response) => {
              if (!response.ok) {
                console.warn("❌ No se pudo cachear:", url);
                return null;
              }
              return cache.put(url, response.clone());
            })
            .catch(() => console.warn("❌ Error cacheando:", url))
        )
      );
    })
  );

  self.skipWaiting();
});

// Activar SW
self.addEventListener("activate", (event) => {
  console.log("[ServiceWorker] Activate");

  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );

  self.clients.claim();
});

//  Interceptar fetch
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached; // devolver cache

      return fetch(event.request)
        .then((response) => response) // fetch normal
        .catch(() => {
          // fallback seguro
          if (event.request.destination === "document") {
            return caches.match("/");
          }

          // *** SIEMPRE devolver una Response válida ***
          return new Response("", { status: 200 });
        });
    })
  );
});
