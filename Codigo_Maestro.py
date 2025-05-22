import serial
import time	
from machine import Pin, UART
import utime

puerto = 'COM3'  # Cambia esto según el puerto donde esté conectada tu Pico
velocidad = 115200  # Velocidad por defecto para MicroPython

# Pines para activar nodos
nodo1_pin = Pin(0, Pin.OUT)
nodo2_pin = Pin(1, Pin.OUT)
mensaje = 0
# UART para recibir datos de los nodos
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  # Asegúrate de conectar RX al TX del nodo

def recibir_rssi():
    if uart.any():
        mensaje = uart.read()  # Leer y decodificar el mensaje
        return mensaje

while True:
    # Activa nodo 1
    nodo1_pin.high()
    utime.sleep(0.1)
    nodo1_pin.low()
    rssi1 = recibir_rssi()

    # Activa nodo 2
    nodo2_pin.high()
    utime.sleep(0.1)
    nodo2_pin.low()
    rssi2 = recibir_rssi()

    print(f"{rssi1}\t{rssi2}")  # Enviado al PC por USB
    utime.sleep(1)
