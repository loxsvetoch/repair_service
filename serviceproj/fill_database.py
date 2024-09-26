
macbooks = [
    'MacBook',
    'MacBook Air',
    'MacBook Pro',
    'MacBook Pro (Retina)',
    'MacBook Pro (Touch Bar)',
    'MacBook Pro (M1)',
    'MacBook Air (Retina)',
    'MacBook Air (M1)',
    'MacBook Pro 13-inch (M1)',
    'MacBook Pro 14-inch (M1 Pro / M1 Max)'
]
macbook_components = {
    'Процессор': 10000,
    'Оперативная память': 3000,
    'Внутренняя память': 4000,
    'Дисплей': 12000,
    'Клавиатура и тачпад': 5000,
    'Батарея': 4000,
    'Жесткий диск или SSD': 6000,
    'Графический ускоритель': 8000,
    'Звуковая система': 3000,
    'Беспроводные модули': 2000,
    'Корпус': 7000,
    'Разъемы и порты': 2000,
    'Операционная система': 1000,
    'Камера (если есть)': 2000
}


iphones = [
    'iPhone 6',
    'iPhone 6S',
    'iPhone SE',
    'iPhone 7',
    'iPhone 8 ',
    'iPhone X',
    'iPhone XS',
    'iPhone XS Max',
    'iPhone XR',
    'iPhone 11',
    'iPhone 11 Pro'
    'iPhone 11 Pro Max',
    'iPhone SE',
    'iPhone 12' ,
    'iPhone 12 mini',
    'iPhone 12 Pro',
    'iPhone 12 Pro Max',
    'iPhone 13',
    'iPhone 13 mini',
    'iPhone 13 Pro',
    'iPhone 13 Pro Max'
]

iphone_components = {
    'Процессор': 5000,
    'Оперативная память': 2000,
    'Внутренняя память': 1500,
    'Дисплей': 8000,
    'Камера': 3000,
    'Датчики': 1000,
    'Беспроводные модули': 1500,
    'GPS-модуль': 1000,
    'Аккумулятор': 2000,
    'Звуковая система': 2500,
    'Кнопки управления': 500,
    'Операционная система': 1000,
    'Корпус и экран': 6000,
    'Антенны': 800,
    'Штекеры и разъемы': 500
}
televisions = [
    'Samsung QLED 1080p',
    'Samsung QLED Q80T 4K UHD',
    'Samsung Crystal UHD TU8000 4K UHD',
    'Samsung Crystal UHD TU7000 4K UHD',
    'Samsung Crystal UHD TU8500 4K UHD',
    'Samsung The Frame 4K UHD',
    'Samsung The Serif 4K UHD',
    'Samsung The Sero 4K UHD',
    'Samsung RU7100 4K UHD',
    'Samsung RU7300 4K UHD',
    'Samsung RU7100 1080p',
    'Samsung RU7300 1080p',
    'Samsung N5300 1080p',
    'Samsung N5200 1080p',
    'Samsung N5003 1080p',
    
    'Sony Bravia A8H OLED 4K UHD',
    'Sony Bravia X900H 4K UHD',
    'Sony Bravia X950H 4K UHD',
    'Sony Bravia X800H 4K UHD',
    'Sony Bravia X750H 4K UHD',
    'Sony Bravia A9G OLED 4K UHD',
    'Sony Bravia X720E 1080p',
    'Sony Bravia X750F 1080p',
    'Sony Bravia X800G 1080p',
    'Sony Bravia X830F 4K UHD',
    'Sony Bravia X850F 4K UHD',
    'Sony Bravia X900F 4K UHD',
    'Sony Bravia X690E 4K UHD',
    
    'LG OLED CX 4K UHD',
    'LG OLED BX 4K UHD',
    'LG NanoCell 85 Series 4K UHD',
    'LG NanoCell 80 Series 4K UHD',
    'LG UN7300 4K UHD',
    'LG UN8500 4K UHD',
    'LG UN7000 4K UHD',
    'LG UN6950 4K UHD',
    'LG UN7300 1080p',
    'LG UN7000 1080p',
    'LG LM5700 1080p', 
    'LG LM5200 1080p',
    'LG LM5000 1080p',
]

television_components = {
    'Дисплей (экран)': 15000,
    'Процессор (для смарт-функций)': 5000,
    'Память (для смарт-функций)': 2000,
    'Аудио-система (динамики)': 3000,
    'Беспроводные модули (Wi-Fi, Bluetooth)': 1500,
    'Пульт дистанционного управления': 1000,
    'Материал корпуса': 4000,
    'Монтажная и структурная архитектура': 5000,
    'Блок питания и электрика': 2000,
    'Дополнительные разъемы и порты': 1000
}

from serviceproj.models import Device, Component
from serviceproj import db


def populate_devices_and_components(devices_list, components_dict, device_type):
    for model in devices_list:
        device = Device(title=model, type=device_type)
        db.session.add(device)
        db.session.commit()

        for component_name, component_cost in components_dict.items():
            component = Component(label=component_name, type='Hardware', device_id=device.id, cost=component_cost)
            db.session.add(component)
        db.session.commit()

# Заполнение данных для макбуков
