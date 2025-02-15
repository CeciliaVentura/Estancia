import network
import espnow
import time
from machine import SoftI2C, Pin
import bno055
from ota import OTAUpdater
from email import enviar_correo
from wifi import conectar_wifi
from config import PEER_MAC

# Conectar a WiFi para OTA y correos
conectar_wifi()

# Ejecutar OTA
ota_updater = OTAUpdater()
ota_updater.download_and_install_update_if_available()

# Configuración I2C para BNO055
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bno = bno055.BNO055(i2c)

# Iniciar ESP-NOW
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)
esp.add_peer(PEER_MAC)

def obtener_datos():
    """Obtiene orientación del BNO055 y datos simulados de GPS."""
    euler = bno.euler()
    latitud = 19.4326  # Simulación
    longitud = -99.1332  # Simulación
    orientacion = euler[0] if euler else 0.0
    return latitud, longitud, orientacion

while True:
    lat, lon, ori = obtener_datos()
    mensaje = f"{lat},{lon},{ori}"
    
    # Enviar por ESP-NOW
    try:
        esp.send(PEER_MAC, mensaje)
        print(f"📡 Datos enviados: {mensaje}")
    except:
        print("❌ Error en el envío ESP-NOW")

    # Enviar por correo
    enviar_correo(mensaje)

    time.sleep(10)

