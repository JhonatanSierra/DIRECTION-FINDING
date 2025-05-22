import serial
import time

puerto = 'COM3'  # Cambia esto según el puerto donde esté conectada tu Pico
velocidad = 115200  # Velocidad por defecto para MicroPython

with serial.Serial(puerto, velocidad, timeout=1) as ser, open("datos.txt", "a", buffering=1) as archivo:
    print("Escuchando en", puerto)
    while True:
        linea = ser.readline().decode().strip()
        if linea:
            print("Recibido:", linea)
            archivo.write(linea + "\n")
            # No es necesario llamar a flush de forma manual en este caso.
