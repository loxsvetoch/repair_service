document.getElementById('service-address').addEventListener('change', function() {
    const serviceAddress = this.value;
    //запрос к фильтрации данных
    fetch('/filter_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `serviceAddress=${encodeURIComponent(serviceAddress)}`
    })
    .then(response => response.json())//вернуть в json
    .then(data => {
        if (data.error) {
            alert(data.error); //Service not found
        } else {
            // Очистить списки
            const devicesDatalist = document.getElementById('devices');
            const servicesDatalist = document.getElementById('workshop_services');
            devicesDatalist.innerHTML = '';
            servicesDatalist.innerHTML = '';

            // Добавить отфильтрованные девайсы
            data.devices.forEach(device => {
                const option = document.createElement('option');
                option.value = device.title;
                devicesDatalist.appendChild(option);
            });
            
            // Добавить отфильтрованные услуги
            data.workshop_services.forEach(service => {
                const option = document.createElement('option');
                option.value = service.description;
                servicesDatalist.appendChild(option);
            });
        }
    });
});