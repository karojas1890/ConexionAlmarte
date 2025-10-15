 function selectDate(element) {
            // Remove selected class from all date options
            document.querySelectorAll('.date-option').forEach(option => {
                option.classList.remove('selected');
            });
            // Add selected class to clicked option
            element.classList.add('selected');
        }

        function selectTime(element) {
            // Remove selected class from all time options
            document.querySelectorAll('.time-option').forEach(option => {
                option.classList.remove('selected');
            });
            // Add selected class to clicked option
            element.classList.add('selected');
        }

        function continueToPayment(button) {
            const selectedDate = document.querySelector('.date-option.selected')?.textContent;
            const selectedTime = document.querySelector('.time-option.selected')?.textContent;
            const paymentUrl = button.getAttribute('data-url');
            localStorage.setItem('selectedDate', selectedDate);
            localStorage.setItem('selectedTime', selectedTime);
    
           // Toma el URL del  del btn
           
            window.location.href = paymentUrl;
        }
