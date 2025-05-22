from machine import Pin, UART
import utime

# Configurar UART1 (puedes usar UART0 si quieres otros pines)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Pin para controlar dirección (DE/RE unidos)
dir_ctrl = Pin(6, Pin.OUT)

# Funciones auxiliares
def enviar_mensaje(mensaje):
    dir_ctrl.value(1)  # Activar modo transmisión
    utime.sleep_us(20) # Pequeña espera para estabilidad
    uart.write(mensaje + '\n')  # Enviar mensaje con nueva línea
    utime.sleep_us(20)
    dir_ctrl.value(0)  # Volver a modo recepción

# Inicialmente, modo recepción
dir_ctrl.value(0)

print("Nodo Pico W listo. Escuchando mensajes...")

contador = 0

while True:
    # Escuchar mensajes entrantes
    if uart.any():
        data = uart.readline()
        if data:
            print("Mensaje recibido:", data.decode().strip())

    # Cada 5 segundos, enviar un mensaje
    if contador % 50 == 0:
        enviar_mensaje("Hola desde nodo RS-485")

    utime.sleep(0.1)
    contador += 1
