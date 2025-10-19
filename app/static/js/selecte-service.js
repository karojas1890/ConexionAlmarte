 function selectService(serviceType) {
          
            localStorage.setItem('selectedService', serviceType);
            
            
            window.location.href = "{{ url_for('routes.select_datetime') }}";
        }

        document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("services-container");

    fetch('/citas/servicios')
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            data.forEach(servicio => {
                const div = document.createElement("div");
                div.className = "service-item";

                // se pasan datos a la funcion
                div.onclick = () => selectService(servicio);

                div.innerHTML = `
                    <div style="overflow: auto;" class="service-info">
                        <div class="service-icon" style="width:100px; height:100px;">
                            <img src="${servicio.urlimagen}"
                                 alt="${servicio.nombreservicio}" 
                                 class="service-icon-img" 
                                 style="width:100%; height:100%; border-radius:20%;"
                            >
                        </div>
                        <div class="service-details">
                            <h3>${servicio.nombreservicio}</h3>
                            <p>Duración: ${servicio.duracionHoras ? servicio.duracionHoras*60 : "N/A"} minutos</p>
                            <p class="service-price">₡${servicio.precio ? servicio.precio.toLocaleString() : "0"}</p>
                        </div>
                    </div>
                    <div class="service-arrow">›</div>
                `;

                container.appendChild(div);
            });
        })
        .catch(err => console.error("Error al cargar servicios:", err));
});

// Guardar el servicio seleccionado y redirigir
function selectService(service) {
    localStorage.setItem('selectedServiceId', service.idservicio);
    localStorage.setItem('selectedServiceName', service.nombreservicio);
     localStorage.setItem('selectedPrice', service.precio);  
    window.location.href = SELECTDATETIME;
}

