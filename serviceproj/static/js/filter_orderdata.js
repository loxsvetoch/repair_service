document.getElementById('service-address').addEventListener('change', function() {
    // Очистить списки до запроса данных
    const devicesDatalist = document.getElementById('devices');
    const servicesDatalist = document.getElementById('workshop_services');
    devicesDatalist.innerHTML = '';
    servicesDatalist.innerHTML = '';

    const serviceAddress = this.value;

    // Проверка на пустой выбор сервиса
    if (!serviceAddress) {
        alert("Пожалуйста, выберите сервис."); // Сообщение об ошибке, если сервис не выбран
        return; // Прекратить выполнение, если сервис не выбран
    }

    // Запрос к серверу для получения новых данных
    fetch('/filter_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `serviceAddress=${encodeURIComponent(serviceAddress)}`
    })
    .then(response => response.json()) // Преобразовать ответ в JSON
    .then(data => {
        if (data.error) {
            alert(data.error); // Сообщение об ошибке, если сервис не найден
        } else {
            // Добавить отфильтрованные устройства
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

window.onload = function() {
    document.getElementById('devices').innerHTML = '';
    document.getElementById('workshop_services').innerHTML = '';
};
