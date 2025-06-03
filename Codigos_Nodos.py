import network
import socket
import time

ID_NODO = 1  # Cambia esto para cada nodo
RED_REFERENCIA = "APCARRITO"

# Configurar Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig((
    f'192.168.1.101{ID_NODO}',  # IP fija
    '255.255.255.0',
    '192.168.1.1',
    '192.168.1.1'
))
wlan.connect('APMAESTRO', '12345678')
print("Conectando al maestro...")

while not wlan.isconnected():
    print("Esperando conexión al maestro...")
    time.sleep(1)

print(f"Nodo {ID_NODO} conectado. IP:", wlan.ifconfig())

# Crear socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
DESTINO = ('192.168.1.100', 5005)

def leer_rssi_red_objetivo():
    redes = wlan.scan()
    #print("Redes detectadas:")
    for red in redes:
        try:
            ssid = red[0].decode()
            print(f"SSID: {ssid}, RSSI: {red[3]}")
            if ssid == RED_REFERENCIA:
                return red[3]
        except:
            continue
    print("No se encontró la red de referencia.")
    return -100

print("Entrando al bucle principal...")

while True:
    valor = leer_rssi_red_objetivo()
    mensaje = f"{ID_NODO}:{valor}"
    print("Enviando:", mensaje)
    udp.sendto(mensaje.encode(), DESTINO)
    time.sleep(2)
