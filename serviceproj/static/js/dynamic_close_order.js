let serviceIndex = 1; // Уникальный индекс для новых услуг

    document.getElementById('add-service').addEventListener('click', function() {
        const newServiceItem = document.createElement('div');
        newServiceItem.classList.add('service-item');

        // Генерируем уникальные ID для нового input и datalist потому что дибил не может собрать все сразу
        const inputId = `service-type-${serviceIndex}`;
        const datalistId = `workshop_services-${serviceIndex}`;

        newServiceItem.innerHTML = `
            <label for="${inputId}">Тип услуги:</label>
            <input type="text" id="${inputId}" name="services[]" list="${datalistId}" placeholder="Выберите тип услуги">
            <datalist id="${datalistId}">
                <!-- Здесь опции будут добавляться через JavaScript -->
            </datalist>
            <button type="button" class="remove-service">-</button>
        `;

        // Добавляем новый элемент в контейнер
        document.getElementById('services').appendChild(newServiceItem);
        serviceIndex++; // Увеличиваем индекс для следующего элемента

        // Добавляем обработчик для кнопки удаления
        newServiceItem.querySelector('.remove-service').addEventListener('click', function() {
            newServiceItem.remove(); // Удаляем элемент service-item
        });

        // Добавляем опции для нового datalist
        addOptionsToDatalist(datalistId);
    });

    document.getElementById('order-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(this);
        const servicesArray = formData.getAll('services[]'); // Получаем массив услуг
        
        const url = window.location.href;
        const taskId = url.split('/').pop(); // Получаем последний элемент из URL
        
        console.log("Услуги, которые будут отправлены:", servicesArray);
        console.log("Order ID (Task ID):", taskId);
        
        // Отправляем данные на сервер
        fetch('/calc_order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ services: servicesArray, order_id: taskId }), // Отправляем услуги и ордер id
        })
        .then(response => {
            if (response.ok) {
                window.location.href = "/profile";
            } else {
                console.error("Ошибка", response.statusText);
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
        });
    });
    
    function addOptionsToDatalist(datalistId) {
        fetch('/filter_workshop_services/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Ошибка:", data.error);
                return;
            }

            const datalist = document.getElementById(datalistId);
            data.forEach(service => {
                const option = document.createElement('option');
                option.value = service.description.concat(" ", service.cost);
                datalist.appendChild(option);
            });
        })
        .catch(error => {
            console.error("Ошибка при получении данных:", error);
        });
    }

    // Инициализация для первого datalist
    addOptionsToDatalist('workshop_services-0');