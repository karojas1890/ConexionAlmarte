 // Configuración global de PayPal
        let ALMARTE_PAYPAL_CONFIG = {
            clientId: 'AZfjbKTM0Mrs69k-q1LtCyqsd36OFn8temhI756Rw5tW6QecVtrGHN5NBABwIGyvrQyu-wiYyoQiG2M3',
            currency: 'USD',
            amount: '0.00',
            description: ''
        };
        
        function almarte_openSINPEModal() {
            const modal = document.getElementById('almarte-sinpe-modal');
            modal.classList.add('active');
            document.getElementById('almarte-sinpe-reference').focus();
        }
        function selectPaymentAndOpenSINPE(element) {
            selectPayment(element);
            almarte_openSINPEModal();
        }
        function almarte_closeSINPEModal() {
            const modal = document.getElementById('almarte-sinpe-modal');
            modal.classList.remove('active');
            document.getElementById('almarte-sinpe-form').reset();
            document.querySelectorAll('.almarte-sinpe-error-msg').forEach(msg => msg.classList.remove('show'));
            document.querySelectorAll('.almarte-sinpe-input').forEach(input => input.classList.remove('error'));
        }

        function almarte_validateSINPE(event) {
            event.preventDefault();

            const reference = document.getElementById('almarte-sinpe-reference').value.trim();
            const phone = document.getElementById('almarte-sinpe-phone').value.trim();
            const amount = document.getElementById('almarte-sinpe-amount').value.trim();

            let isValid = true;

            
            document.querySelectorAll('.almarte-sinpe-error-msg').forEach(msg => msg.classList.remove('show'));
            document.querySelectorAll('.almarte-sinpe-input').forEach(input => input.classList.remove('error'));

            
            if (!reference || reference.length < 4) {
                almarte_showError('almarte-sinpe-reference', 'El número de referencia debe tener al menos 6 caracteres');
                isValid = false;
            } else if (!/^[a-zA-Z0-9]+$/.test(reference)) {
                almarte_showError('almarte-sinpe-reference', 'Solo se permiten números y letras');
                isValid = false;
            }

            
            if (!phone || phone.length < 8) {
                almarte_showError('almarte-sinpe-phone', 'Ingresa un número de teléfono válido');
                isValid = false;
            } else if (!/^[0-9]+$/.test(phone)) {
                almarte_showError('almarte-sinpe-phone', 'Solo se permiten números');
                isValid = false;
            }

            
            const summaryAmount = document.getElementById('summary-price')?.textContent || '';
            
            
            if (!amount || parseInt(amount) <= 0) {
                almarte_showError('almarte-sinpe-amount', 'Ingresa un monto válido');
                isValid = false;
            } 
            if (isValid) {
                almarte_submitSINPE(reference, phone, amount);
            }
        }

        function almarte_showError(inputId, message) {
            const input = document.getElementById(inputId);
            const errorMsg = document.getElementById(inputId + '-error');
            input.classList.add('error');
            errorMsg.textContent = message;
            errorMsg.classList.add('show');
        }

        function almarte_submitSINPE(reference, phone, amount) {
            const submitBtn = document.getElementById('almarte-sinpe-submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Validando...';

            
            fetch(SINPE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nreferencia: reference,
                    ntelefono: phone,
                    monto: amount
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.valido) {
                    almarte_showSINPESuccess();
                    localStorage.setItem('sinpeValidated', 'true');
                    localStorage.setItem('sinpeReference', reference);
                    continueToPaymentForm();
                } else {
                    almarte_showError('almarte-sinpe-reference', data.message || 'No se pudo validar el SINPE. Intenta de nuevo.');
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Validar SINPE';
                }
            })
            .catch(error => {
                console.error('[v0] SINPE validation error:', error);
                almarte_showError('almarte-sinpe-reference', 'Error de conexión. Intenta de nuevo.');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Validar SINPE';
            });
        }

        function almarte_showSINPESuccess() {
            const modal = document.getElementById('almarte-sinpe-modal');
            const content = document.querySelector('.almarte-sinpe-modal-content');
            
            const successHTML = `
                <div class="almarte-sinpe-success">
                    <div class="almarte-sinpe-success-icon">✓</div>
                    <div class="almarte-sinpe-success-text">¡SINPE Validado!</div>
                    <div class="almarte-sinpe-success-subtext">Tu pago ha sido confirmado correctamente</div>
                </div>
                <div class="almarte-sinpe-buttons">
                    <button class="almarte-sinpe-btn almarte-sinpe-btn-submit" onclick="almarte_confirmSINPE()" style="width: 100%;">
                        Continuar
                    </button>
                </div>
            `;
            
            content.innerHTML = successHTML;
        }

        function almarte_confirmSINPE() {
            almarte_closeSINPEModal();
            showConfirmation();
        }

        // Variable global para el tipo de cambio
        let tipoCambioVenta = 0;

        // Variable global para guardar la opción de pago
        window.selectedPayment = 'Tarjeta de crédito o débito';

        // Función para obtener el tipo de cambio
        async function obtenerTipoCambio() {
            try {
                const response = await fetch(TC_URL); 
                const data = await response.json();

                if (data.compra && data.venta) {
                    tipoCambioVenta = parseFloat(data.venta);
                    console.log("Tipo de cambio obtenido:", tipoCambioVenta);
                    return tipoCambioVenta;
                } else {
                    console.error("No se pudo obtener el tipo de cambio:", data.error);
                    return 580; // Valor por defecto si falla
                }
            } catch (error) {
                console.error("Error al consultar el tipo de cambio:", error);
                return 580; // Valor por defecto si falla
            }
        }

        // Función para convertir colones a dólares
        function convertirColonesADolares(montoColones, tipoCambio) {
            return (montoColones / tipoCambio).toFixed(2);
        }

        // Función para inicializar PayPal con el monto calculado
        function inicializarPayPal(montoUSD, descripcion) {
            ALMARTE_PAYPAL_CONFIG.amount = montoUSD;
            ALMARTE_PAYPAL_CONFIG.description = descripcion;

            if (typeof paypal === 'undefined') {
                console.log("PayPal SDK no cargado, reintentando...");
                setTimeout(() => inicializarPayPal(montoUSD, descripcion), 500);
                return;
            }

            // Limpiar contenedor anterior
            const container = document.getElementById('almarte-paypal-button-container');
            container.innerHTML = '';

            try {
                paypal.Buttons({
                    style: {
                        shape: 'rect',
                        color: 'gold',
                        layout: 'vertical',
                        label: 'paypal',
                        height: 48
                    },
                    createOrder: function(data, actions) {
                       
                        return actions.order.create({
                            purchase_units: [{
                                amount: {
                                    value: ALMARTE_PAYPAL_CONFIG.amount,
                                    currency_code: ALMARTE_PAYPAL_CONFIG.currency
                                },
                                description: ALMARTE_PAYPAL_CONFIG.description
                            }]
                        });
                    },
                    onApprove: function(data, actions) {
                        return actions.order.capture().then(function(orderData) {
                            console.log("Pago PayPal completado:", orderData);
                            procesarPagoPayPalExitoso(orderData);
                        });
                    },
                    onError: function(err) {
                        console.error("Error en PayPal:", err);
                        almarte_showErrorModal('Error en el pago: ' + err.message);
                    },
                    onCancel: function(data) {
                        console.log("Pago PayPal cancelado");
                    }
                }).render('#almarte-paypal-button-container');
                
                console.log("Botones de PayPal inicializados con:", montoUSD + " USD");
            } catch (error) {
                console.error("Error al inicializar PayPal:", error);
            }
        }

        // Función para procesar pago exitoso de PayPal
        function procesarPagoPayPalExitoso(orderData) {
            const selectedService = localStorage.getItem('selectedServiceName') || "Servicio no definido";
            const selectedDate = localStorage.getItem("selectedDate");
            const selectedTime = localStorage.getItem("selectedTime");
            const selectedPrice = parseFloat(localStorage.getItem("selectedPrice")) || 0;
            const servicio = parseInt(localStorage.getItem("selectedServiceId"));
            const iddisponibilidad = parseInt(localStorage.getItem("idDisponibilidadSeleccionada"));

            const citaData = {
                usuario,
                servicio,
                iddisponibilidad,
                estado: 1,
                pago: 2, // 2 = pago con PayPal
                id_transaccion_paypal: orderData.id,
                monto_paypal_usd: ALMARTE_PAYPAL_CONFIG.amount
            };

            // Crear la cita después del pago exitoso
            fetch(CITA_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(citaData)
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    almarte_showErrorModal("Error al crear la cita: " + data.error);
                } else {
                    almarte_showSuccessModal(orderData, selectedDate, selectedTime, selectedPrice);
                }
            })
            .catch(err => {
                console.error("Error al crear cita:", err);
                almarte_showErrorModal("Error al procesar la cita");
            });
        }

        // Modal de éxito para PayPal
        function almarte_showSuccessModal(orderData, fecha, hora, precio) {
            const selectedService = localStorage.getItem('selectedServiceName') || "Servicio no definido";

            const modal = document.createElement('div');
            modal.innerHTML = `
                <div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000;">
                    <div style="background: white; border-radius: 15px; padding: 30px; max-width: 320px; text-align: center;">
                        <div style="width: 60px; height: 60px; background: #4CAF50; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; color:white; font-size:30px;">✓</div>
                        <h3>¡Pago exitoso!</h3>
                        <p>Tu pago con PayPal se procesó correctamente y tu cita ha sido confirmada.</p>
                        <div style="background:#f5f5f5; padding:15px; border-radius:8px; margin:15px 0; text-align:left;">
                            <p><strong>Servicio:</strong> ${selectedService}</p>
                            <p><strong>Fecha:</strong> ${fecha}</p>
                            <p><strong>Hora:</strong> ${hora}</p>
                            <p><strong>Total pagado:</strong> $${ALMARTE_PAYPAL_CONFIG.amount} USD</p>
                            <p><strong>Equivalente:</strong> ₡${precio.toLocaleString()} CRC</p>
                            <p><strong>ID Transacción:</strong> ${orderData.id.substring(0, 10)}...</p>
                        </div>
                        <button onclick="almarte_closeModal(true)" style="background:#5f9ea0; color:white; border:none; border-radius:20px; padding:12px 30px; cursor:pointer; width:100%;">Entendido</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        // Modal de error para PayPal
        function almarte_showErrorModal(message) {
            const modal = document.createElement('div');
            modal.innerHTML = `
                <div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000;">
                    <div style="background: white; border-radius: 15px; padding: 30px; max-width: 320px; text-align: center;">
                        <div style="width: 60px; height: 60px; background: #f44336; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; color:white; font-size:30px;">✕</div>
                        <h3>Error en el pago</h3>
                        <p>${message}</p>
                        <button onclick="almarte_closeModal(false)" style="background:#5f9ea0; color:white; border:none; border-radius:20px; padding:12px 30px; cursor:pointer; width:100%;">Reintentar</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        function almarte_closeModal(success) {
            const modal = document.querySelector('[style*="position: fixed"]');
            if (modal) modal.remove();
            if (success) {
                setTimeout(() => {
                    window.location.href = dashboardUrl;
                }, 1000);
            }
        }

        // Mostrar resumen de la cita al cargar la página
        document.addEventListener("DOMContentLoaded", async () => {
            const selectedService = localStorage.getItem('selectedServiceName') || "No seleccionado";
            const selectedPrice = parseFloat(localStorage.getItem('selectedPrice')) || 0;
            const selectedDate = localStorage.getItem("selectedDate") || "No definida";
            const selectedTime = localStorage.getItem("selectedTime") || "No definida";

            // Obtener tipo de cambio
            const tipoCambio = await obtenerTipoCambio();
            
            // Calcular equivalente en USD
            const montoUSD = convertirColonesADolares(selectedPrice, tipoCambio);
            
            // Mostrar datos en el resumen
            document.getElementById('service-summary-text').textContent = selectedService;
            document.getElementById('summary-price').textContent = `₡${!isNaN(selectedPrice) ? selectedPrice.toLocaleString() : "0"}`;
            document.getElementById('summary-date').textContent = selectedDate;
            document.getElementById('summary-time').textContent = selectedTime;
            
            // Mostrar equivalente en USD si es mayor a 0
            if (selectedPrice > 0) {
                document.getElementById('summary-usd').textContent = `$${montoUSD} USD`;
                document.getElementById('usd-equivalent').style.display = 'flex';
                
                // Mostrar información de tipo de cambio
                document.getElementById('paypal-exchange-rate').textContent = 
                    `Tipo de cambio: $1 USD = ₡${tipoCambio.toFixed(2)} CRC`;
                
                // Inicializar PayPal con el monto calculado
                inicializarPayPal(montoUSD, selectedService);
            }
        });

        // Función para seleccionar método de pago
        window.selectPayment = function(element) {
            document.querySelectorAll('.payment-option').forEach(option => option.classList.remove('selected'));
            element.classList.add('selected');
            window.selectedPayment = element.querySelector('.payment-text').innerText;
            
        }
        // Función al continuar con el pago (para otros métodos)
        function continueToPaymentForm() {
            const servicio = parseInt(localStorage.getItem("selectedServiceId"));
            const iddisponibilidad = parseInt(localStorage.getItem("idDisponibilidadSeleccionada"));
            const selectedDate = localStorage.getItem("selectedDate");
            const selectedTime = localStorage.getItem("selectedTime");
            const selectedPrice = parseFloat(localStorage.getItem("selectedPrice")) || 0;

            const citaData = {
                usuario,
                servicio,
                iddisponibilidad,
                estado: 1,
                pago: 1 // 1 = pago con tarjeta o efectivo según selección
            };

            if (window.selectedPayment === 'Tarjeta de crédito o débito') {
                window.location.href = paymentforUrl;
            } else {
                fetch(CITA_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(citaData)
                })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert("Error: " + data.error);
                    } else {
                        showConfirmation(selectedDate, selectedTime, selectedPrice);
                    }
                })
                .catch(err => console.error("Error al crear cita:", err));
            }
        }

        // Modal de confirmación para otros métodos de pago
        function showConfirmation(fecha, hora, precio) {
            const selectedService = localStorage.getItem('selectedServiceName') || "Servicio no definido";

            const modal = document.createElement('div');
            modal.innerHTML = `
                <div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000;">
                    <div style="background: white; border-radius: 15px; padding: 30px; max-width: 320px; text-align: center;">
                        <div style="width: 60px; height: 60px; background: #4CAF50; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; color:white; font-size:30px;">✓</div>
                        <h3>Cita confirmada!</h3>
                        <p>Tu cita ha sido agendada exitosamente. Te enviaremos los detalles por email.</p>
                        <div style="background:#f5f5f5; padding:15px; border-radius:8px; margin:15px 0; text-align:left;">
                            <p><strong>Servicio:</strong> ${selectedService}</p>
                            <p><strong>Fecha:</strong> ${fecha}</p>
                            <p><strong>Hora:</strong> ${hora}</p>
                            <p><strong>Total:</strong> ₡${precio.toLocaleString()}</p>
                        </div>
                        <button onclick="closeModal()" style="background:#5f9ea0; color:white; border:none; border-radius:20px; padding:12px 30px; cursor:pointer;">Entendido</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        function closeModal() {
            const modal = document.querySelector('[style*="position: fixed"]');
            if (modal) modal.remove();
            window.location.href = dashboardUrl;
        }