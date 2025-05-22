from machine import Pin, UART
import utime
import random

# Configurar el pin con resistencia de pull-down
pin_activador = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Cambiar a otro pin para Nodo 2
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  # TX al RX del maestro
n = 0
estado_anterior = 0

def simular_rssi():
    return random.randint(-90, -30)

def leer_pin_estable(pin):
    """Filtra fluctuaciones en el pin de entrada, asegurando que el estado sea estable."""
    estado = pin.value()
    utime.sleep(0.01)  # Espera pequeña para evitar fluctuaciones
    print("estable", n)
    return pin.value() == estado

while True:
    estado_actual = pin_activador.value()
    
    # Verificar flanco ascendente (de 0 a 1) y si el pin mantiene el estado
    if estado_actual == 1 and estado_anterior == 0 and leer_pin_estable(pin_activador):
        rssi = simular_rssi()
        uart.write(f"{rssi}\n")
        print("if", n)
        n = n + 1
    
    estado_anterior = estado_actual
    utime.sleep(0.05)  # Tiempo de espera para evitar lecturas rápidas
