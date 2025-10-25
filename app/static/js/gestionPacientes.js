// Modal functions
        function openAddPatientModal() {
            document.getElementById('addPatientModal').classList.add('active');
        }

        function closeAddPatientModal() {
            document.getElementById('addPatientModal').classList.remove('active');
            document.getElementById('addPatientForm').reset();
        }


        // Search functionality
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const patientCards = document.querySelectorAll('.patient-card');
            
            patientCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });

        // Close modal when clicking outside
        document.getElementById('addPatientModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeAddPatientModal();
            }
        });

async function submitPatient() {
  const data = {
    identificacion: document.getElementById("identification").value,
    nombre: document.getElementById("nombre").value,
    primerApellido: document.getElementById("apellido1").value,
    segundoApellido: document.getElementById("apellido2").value,
    telefono: document.getElementById("telefono").value,
    fechaNacimiento: document.getElementById("fechaNacimiento").value,
    provincia: document.getElementById("provincia").value,
    canton: document.getElementById("canton").value,
    distrito: document.getElementById("distrito").value,
    direccion: document.getElementById("direccion").value,
    edad: document.getElementById("edad").value,
    lugarTrabajo: document.getElementById("lugarTrabajo").value,
    ocupacion: document.getElementById("ocupacion").value,
    correo: document.getElementById("correo").value
    
  };

  try {
    const res = await fetch("/usuarios/crear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (!res.ok) {
      alert("Error: " + result.error);
      return;
    }

    alert("Usuario creado: " + result.usuario + "\nContraseña: " + result.contrasena);
    document.getElementById("addPatientForm").reset();
    closeAddPatientModal();

  } catch (error) {
    console.error("Error al crear usuario:", error);
    alert("Ocurrió un error al crear el usuario.");
  }
}


        

document.addEventListener("DOMContentLoaded", async () => {
  const provinceSelect = document.getElementById("provincia");
  const cantonSelect = document.getElementById("canton");
  const districtSelect = document.getElementById("distrito");

  const provinciasURL = "/static/Data/geoBoundaries-CRI-ADM1_simplified.geojson";
  const cantonesURL   = "/static/Data/geoBoundaries-CRI-ADM2_simplified.geojson";
  const distritosURL  = "/static/Data/geoBoundaries-CRI-ADM3_simplified.geojson";

  // Cargar los 3 GeoJSON en paralelo
  const [provinciasData, cantonesData, distritosData] = await Promise.all([
    fetch(provinciasURL).then(r => r.json()),
    fetch(cantonesURL).then(r => r.json()),
    fetch(distritosURL).then(r => r.json())
  ]);

  
  // Preparar arrays
  const provinces = provinciasData.features;
  const cantons = cantonesData.features;
  const districts = distritosData.features;

  // calcula centroid para cada canton y district solo una vez
  cantons.forEach(f => {
    // turf.centroid devuelve un Feature(Point)
    try { f._centroid = turf.centroid(f); } catch(e){ f._centroid = null; }
  });
  districts.forEach(f => {
    try { f._centroid = turf.centroid(f); } catch(e){ f._centroid = null; }
  });

  // Construir mapa: provinceISO -> { name, features, cantons: { cantonID: { ... , districts: [...] } } }
  const hierarchy = {};

  provinces.forEach(p => {
    const code = p.properties.shapeName;
    hierarchy[code] = {
      name: (p.properties.shapeName || "").replace(/^Provincia\s+/i,""),
      feature: p,
      cantons: {}
    };
  });

  // Asigna cada canton a una provincia comprobando si su centroid esta dentro de la provincia
  cantons.forEach(c => {
    if (!c._centroid) return;
    let assigned = false;
    for (const p of provinces) {
      try {
        if (turf.booleanPointInPolygon(c._centroid, p)) {
          const pcode = p.properties.shapeName;
          const cid = c.properties.shapeName;
          hierarchy[pcode].cantons[cid] = {
            name: c.properties.shapeName,
            feature: c,
            districts: {}
          };
          assigned = true;
          break;
        }
      } catch(e){ /* ignore geometry errors */ }
    }
    // Si no se asigno, lo pone en un bucket sin-provincia 
    if (!assigned) {
      const pcode = "SIN_PROVINCIA";
      if (!hierarchy[pcode]) hierarchy[pcode] = { name: "Sin provincia", cantons: {} };
      const cid =c.properties.shapeName;
      hierarchy[pcode].cantons[cid] = { name: c.properties.shapeName, feature: c, districts: {} };
    }
  });

  // Asignaa distritos a cantones de forma similar centroid dentro del canton
  districts.forEach(d => {
    if (!d._centroid) return;
    let assigned = false;
    // recorrer todas las provincias y cantones en hierarchy
    for (const pkey of Object.keys(hierarchy)) {
      const p = hierarchy[pkey];
      for (const ckey of Object.keys(p.cantons)) {
        const cantonFeature = p.cantons[ckey].feature;
        try {
          if (turf.booleanPointInPolygon(d._centroid, cantonFeature)) {
            p.cantons[ckey].districts[ d.properties.shapeName] = {
              name: d.properties.shapeName,
              feature: d
            };
            assigned = true;
            break;
          }
        } catch(e){ /* ignore geometry errors */ }
      }
      if (assigned) break;
    }
    if (!assigned) {
      // si no se asigno lo dejama en un bucket es decir sin-canton
      const pcode = "SIN_PROVINCIA";
      if (!hierarchy[pcode]) hierarchy[pcode] = { name: "Sin provincia", cantons: {} };
      const cid = "SIN_CANTON";
      if (!hierarchy[pcode].cantons[cid]) hierarchy[pcode].cantons[cid] = { name: "Sin cantón", districts: {} };
      hierarchy[pcode].cantons[cid].districts[d.properties.shapeName] = {
        name: d.properties.shapeName,
        feature: d
      };
    }
  });

  // --- Poblar selects ---
  // Provincias
  provinceSelect.innerHTML = '<option value="">Seleccionar...</option>';
  Object.keys(hierarchy).forEach(pcode => {
    const p = hierarchy[pcode];
    
    if (pnameIsEmpty(p.name)) return;
    const opt = document.createElement("option");
    opt.value = pcode;
    opt.textContent = p.name;
    provinceSelect.appendChild(opt);
  });

  // Cuando selecciona provincia llena cantones
  provinceSelect.addEventListener("change", () => {
    const selectedProvinceCode = provinceSelect.value;
    cantonSelect.innerHTML = '<option value="">Seleccionar...</option>';
    districtSelect.innerHTML = '<option value="">Seleccionar...</option>';
    if (!selectedProvinceCode) return;
    const p = hierarchy[selectedProvinceCode];
    Object.keys(p.cantons).forEach(ckey => {
      const c = p.cantons[ckey];
      const opt = document.createElement("option");
      opt.value = c.feature.properties.shapeName;
      opt.textContent = c.name;
      cantonSelect.appendChild(opt);
    });
  });

  // Cuando selecciona canton llena distritos 
  cantonSelect.addEventListener("change", () => {
    const selectedProvinceCode = provinceSelect.value;
    const selectedCantonName = cantonSelect.options[cantonSelect.selectedIndex]?.text || "";
    districtSelect.innerHTML = '<option value="">Seleccionar...</option>';
    if (!selectedProvinceCode || !selectedCantonName) return;
    const p = hierarchy[selectedProvinceCode];
    // aqui buscar el canton por nombre porque el value puede ser shapeID
    const cantonEntry = Object.values(p.cantons).find(c => c.name === selectedCantonName);
    if (!cantonEntry) return;
    Object.keys(cantonEntry.districts).forEach(dkey => {
      const d = cantonEntry.districts[dkey];
      const opt = document.createElement("option");
      opt.value = d.feature.properties.shapeName;
      opt.textContent = d.name;
      districtSelect.appendChild(opt);
    });
  });

  // Helper: omitir nombres vacios/buckets tecnicos
  function pnameIsEmpty(name) {
    if (!name) return true;
    const normalized = name.toString().trim().toLowerCase();
    return normalized === "" || normalized === "sin provincia" || normalized === "undefined";
  }

  

});

