
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

washing_machines = [
    'Samsung EcoBubble WW80K5410WW 8kg',
    'Samsung AddWash WW90K6414QW 9kg',
    'Samsung QuickDrive WW90T986DSH 9kg',
    'Samsung EcoBubble WW10T684DLH 10kg',
    'Samsung AddWash WD80K5410OW 8kg',
    'Samsung QuickDrive WD10T654DBH 10kg',
    
    'LG TurboWash F4V9RWP2E 10kg',
    'LG AI DD F2V9HP2W 8kg',
    'LG TwinWash FH4G1BCS2 12kg',
    'LG TurboWash F4V5VYP2T 9kg',
    'LG AI DD F2V5VYP3E 8.5kg',
    'LG Direct Drive F2V3WY3WE 7kg',
    
    'Bosch Serie 6 WAT286H0GB 9kg',
    'Bosch Serie 8 WAW325H0GB 9kg',
    'Bosch HomeProfessional WAYH8790GB 9kg',
    
    'Siemens iQ700 WM14T790GB 9kg',
    'Siemens iQ500 WM14UT93GB 9kg',
    'Siemens iQ500 WM14U640GB 8kg',
    
    'Electrolux PerfectCare 800 EW8F8661BI 10kg',
    'Electrolux PerfectCare 600 EW6F528S 8kg',
    'Electrolux PerfectCare 700 EW7F4722LB 7kg',
    'Electrolux UltraCare Eco EWF1486GDW 8kg'
]


from serviceproj.models import Device, Component
from serviceproj import db


def populate_devices(devices_list, device_type):

    for model in devices_list:
        
        device = Device(title=model, type=device_type)
        db.session.add(device)

        db.session.commit()


def fill_device_components():  
    populate_devices(televisions, "телевизоры")
    populate_devices(macbooks, "ноутбуки")
    populate_devices(iphones, "смартфоны")
    populate_devices(washing_machines, "стиральная машины")
