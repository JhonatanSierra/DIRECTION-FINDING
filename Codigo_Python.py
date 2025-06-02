import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import re

class SimuladorTrilateracion:
    def _init_(self, puerto='COM3', baudios=9600):
        self.num_nodos = 8
        self.lado = 10.0
        self.ruta_guardado = "resultados_trilateracion.txt"
        self.posiciones_nodos = self.generar_posiciones_nodos()
        self.magnitudes_rssi = np.full(self.num_nodos, -100.0)
        self.serial = serial.Serial(puerto, baudios, timeout=1)
        time.sleep(2)  # esperar a que se estabilice la conexión
        self.fig, self.ax = plt.subplots()
        self.anim = None
        self.posicion_anterior = None  # Guardar la posición anterior
        print("Conectado al puerto:", puerto)

    def generar_posiciones_nodos(self):
        return np.array([
            [0, 0],
            [self.lado, 0],
            [self.lado, self.lado],
            [0, self.lado],
            [self.lado / 2, 0],
            [self.lado, self.lado / 2],
            [self.lado / 2, self.lado],
            [0, self.lado / 2]
        ])

    def leer_rssi_serial(self):

        try:
            while self.serial.in_waiting:
                linea = self.serial.readline().decode('utf-8').strip()
                print("Serial recibido:", linea)

            # Acepta R1=-65 o R1: -65
                match = re.match(r"R(\d+)\s*[:=]\s*(-?\d+)", linea)
                if match:
                    idx = int(match.group(1)) - 1
                    valor_rssi = float(match.group(2))
                    if 0 <= idx < self.num_nodos:
                        self.magnitudes_rssi[idx] = valor_rssi
                        print(f"RSSI actualizado: R{idx+1} = {valor_rssi}")
        except Exception as e:
            print("Error al leer desde el puerto serial:", e)


    def convertir_rssi_a_distancia(self, rssi):
        A = -50  # valor de referencia
        n = 2.0  # exponente de pérdida
        return 10 ** ((A - rssi) / (10 * n))

    def estimar_posicion(self):
        print("RSSI actuales:", self.magnitudes_rssi)
        indices_validos = self.magnitudes_rssi > -99
        print(f"RSSI válidos: {np.sum(indices_validos)} / {self.num_nodos}")

        print(f"RSSI válidos: {np.sum(indices_validos)} / {self.num_nodos}")
    
        posiciones_validas = self.posiciones_nodos[indices_validos]
        rssi_validos = self.magnitudes_rssi[indices_validos]

        if len(posiciones_validas) < 3:
            print("No hay suficientes nodos válidos para estimar posición.")
            return np.array([-1, -1])

        distancias = self.convertir_rssi_a_distancia(rssi_validos)
        pesos = 1 / (distancias + 1e-6)
        pesos /= np.sum(pesos)
        return np.average(posiciones_validas, axis=0, weights=pesos)

    
    def actualizar(self, frame):
        self.ax.clear()
        self.ax.set_xlim(-1, self.lado + 1)
        self.ax.set_ylim(-1, self.lado + 1)
        self.ax.set_title("Trilateración con Lectura Serial")

        self.leer_rssi_serial()
        self.ax.plot(self.posiciones_nodos[:, 0], self.posiciones_nodos[:, 1], 'ro', label="Nodos")

        for i, rssi in enumerate(self.magnitudes_rssi):
            if rssi > -100:
                distancia = self.convertir_rssi_a_distancia(rssi)
                circulo = plt.Circle(self.posiciones_nodos[i], distancia, color='b', fill=False, alpha=0.3)
                self.ax.add_patch(circulo)

        estimacion = self.estimar_posicion()
        if estimacion[0] >= 0:
            # Dibujar línea desde la posición anterior
            if self.posicion_anterior is not None:
                self.ax.plot(
                    [self.posicion_anterior[0], estimacion[0]],
                    [self.posicion_anterior[1], estimacion[1]],
                    'k--', alpha=0.5, label="Trayectoria"
                )
                self.ax.plot(*self.posicion_anterior, 'yo', label="Anterior")

            self.ax.plot(*estimacion, 'go', label="Estimación")
            self.posicion_anterior = estimacion.copy()

            with open(self.ruta_guardado, "a") as f:
                f.write(f"{estimacion[0]:.2f},{estimacion[1]:.2f}\n")
        else:
            self.ax.text(self.lado / 2, self.lado - 0.5, "Esperando al menos 3 nodos...", color='red', ha='center')

        self.ax.legend()

    def iniciar_animacion(self):
        self.anim = FuncAnimation(self.fig, self.actualizar, interval=1000)
        plt.show()


# Ejecutar
if _name_ == "_main_":
    simulador = SimuladorTrilateracion(puerto='COM3')  # Cambia COM3 si usas otro puerto
    simulador.iniciar_animacion()
