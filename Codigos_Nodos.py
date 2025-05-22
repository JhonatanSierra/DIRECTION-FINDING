from machine import Pin, UART
import utime

# UART para RS-485
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Control de dirección RS-485 (DE + RE unidos)
dir_ctrl = Pin(6, Pin.OUT)
dir_ctrl.value(0)  # Modo recepción por defecto

# Pin que recibe la señal del maestro
pin_senal = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Estado previo del pin
estado_anterior = 0

# Identificador único del nodo (puede ser diferente por nodo)
NODO_ID = "Nodo 2"

def enviar_mensaje():
    dir_ctrl.value(1)        # Activar transmisión
    utime.sleep_us(20)
    uart.write(f"Mensaje de {NODO_ID}\n")
    utime.sleep_us(20)
    dir_ctrl.value(0)        # Volver a recepción (por seguridad)

print(f"{NODO_ID} listo. Esperando señal para transmitir...")

while True:
    estado_actual = pin_senal.value()

    # Flanco ascendente: de 0 a 1
    if estado_actual == 1 and estado_anterior == 0:
        print("Señal recibida. Enviando mensaje...")
        enviar_mensaje()

    estado_anterior = estado_actual
    utime.sleep(0.05)
