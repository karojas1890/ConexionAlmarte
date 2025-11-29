let compra = 0, venta = 0;
    
async function cargarDatos() {
  try {
    const response = await fetch(URL_TIPOCAMBIO); 
    const data = await response.json();

    if (data.compra && data.venta) {
      // CONVERTIR A NÚMERO - Esto soluciona el error
      compra = parseFloat(data.compra);
      venta = parseFloat(data.venta);
      
      document.getElementById("compra").textContent = "₡" + compra.toFixed(2);
      document.getElementById("venta").textContent = "₡" + venta.toFixed(2);
    } else {
      document.getElementById("compra").textContent = "--";
      document.getElementById("venta").textContent = "--";
      console.error("No se pudo obtener el tipo de cambio:", data.error);
    }
  } catch (error) {
    console.error("Error al consultar el tipo de cambio:", error);
    document.getElementById("compra").textContent = "--";
    document.getElementById("venta").textContent = "--";
  }
}

// Botón para actualizar
document.getElementById("actualizar").addEventListener("click", cargarDatos);

// Conversión de CRC a USD
document.getElementById("aUSD").addEventListener("click", function() {
  let colones = parseFloat(document.getElementById("colones").value);
  if (!isNaN(colones) && venta > 0) {
    document.getElementById("resultado").textContent = "$" + (colones / venta).toFixed(2);
  } else {
    document.getElementById("resultado").textContent = "Error en la conversión";
  }
});

// Conversión de USD a CRC
document.getElementById("aCRC").addEventListener("click", function() {
  let dolares = parseFloat(document.getElementById("dolares").value);
  if (!isNaN(dolares) && compra > 0) {
    document.getElementById("resultado").textContent = "₡" + (dolares * compra).toFixed(2);
  } else {
    document.getElementById("resultado").textContent = "Error en la conversión";
  }
});

// Carga inicial
cargarDatos();