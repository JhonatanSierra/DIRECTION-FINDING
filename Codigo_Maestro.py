import utime
import time
import network
import socket

timeout = 10  # segundos
start = time.time()
# Configurar Wi-Fi con IP fija
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig((
    '192.168.1.100',  # IP del maestro
    '255.255.255.0',
    '192.168.1.1',
    '192.168.1.1'
))
wlan.connect('APMAESTRO', '12345678')

#while not wlan.isconnected():
#    if time.time() - start > timeout:
#        print("❌ No se pudo conectar al Wi-Fi.")
#        break
#    time.sleep(0.5)

while not wlan.isconnected():
    print("No conectado")
    utime.sleep(0.5)
    pass

print('Maestro conectado. IP:', wlan.ifconfig())

# Crear socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('0.0.0.0', 5005))  # Escuchar en el puerto 5005

valores_nodos = [None] * 9  # ID de nodos: 1 a 8

print("Esperando datos de los nodos...")

while True:
    data, addr = udp.recvfrom(1024)
    try:
        mensaje = data.decode().strip()
        #print(f"Recibido: {mensaje} desde {addr}")
        
        id_str, valor_str = mensaje.split(":")
        nodo_id = int(id_str)
        
        if 1 <= nodo_id <= 8:
            valores_nodos[nodo_id] = valor_str
            print(f"R{nodo_id} = {valor_str}")
            #print(f"Nodo {nodo_id} = {valor_str})
        else:
            print("ID fuera de rango")
    
    except Exception as e:
        print("Error:", e)

    #print("Valores actuales:", valores_nodos[1:])
