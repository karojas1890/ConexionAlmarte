 function selectService(serviceType) {
          
            localStorage.setItem('selectedService', serviceType);
            
            
            window.location.href = "{{ url_for('routes.select_datetime') }}";
        }