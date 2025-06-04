import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import re

class SimuladorTrilateracion:
    def __init__(self, puerto='COM8', baudios=9600):
        self.num_nodos = 8
        self.lado = 10.0
        self.radio = 5.0  # Radio del círculo
        self.posiciones_nodos = self.generar_posiciones_nodos()
        self.magnitudes_rssi = np.full(self.num_nodos, -100.0)
        self.rssi_filtrado = np.full(self.num_nodos, -100.0)
        self.serial = serial.Serial(puerto, baudios, timeout=1)
        time.sleep(2)
        self.fig = plt.figure(figsize=(10, 5))
        self.ax_radar = self.fig.add_subplot(1, 2, 1, polar=True)
        self.ax_barras = self.fig.add_subplot(1, 2, 2)
        self.anim = None
        self.direccion_actual = "Este-8m"  # <<< Aquí defines la dirección actual
        print(f"Conectado al puerto serial {puerto}")

    def generar_posiciones_nodos(self):
        angulos = np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315])
        return np.array([[self.radio + self.radio * np.cos(a), self.radio + self.radio * np.sin(a)] for a in angulos])

    def leer_rssi_serial(self):
        try:
            while self.serial.in_waiting:
                linea = self.serial.readline().decode('utf-8').strip()
                print("Serial recibido:", linea)
                match = re.match(r"R(\d+)\s*[:=]\s*(-?\d+)", linea)
                if match:
                    idx = int(match.group(1)) - 1
                    valor_rssi = float(match.group(2))
                    if 0 <= idx < self.num_nodos:
                        alpha = 1.0  # Sin suavizado para prueba
                        self.rssi_filtrado[idx] = alpha * valor_rssi + (1 - alpha) * self.rssi_filtrado[idx]
                        self.magnitudes_rssi[idx] = valor_rssi
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        with open(f"{self.direccion_actual}.txt", "a") as f:
                            f.write(f"{timestamp} - R{idx+1}: {valor_rssi}\n")
        except Exception as e:
            print("Error al leer desde el puerto serial:", e)

    def obtener_direccion_por_rssi_maximo(self):
        idx_max = np.argmax(self.rssi_filtrado)
        print(f"Nodo con mayor RSSI: R{idx_max+1}, RSSI: {self.rssi_filtrado[idx_max]}")
        return idx_max

    def calcular_angulo_desde_nodo(self, idx):
        angulo = np.deg2rad(idx * 45)
        return angulo

    def actualizar(self, frame):
        self.ax_radar.clear()
        self.ax_barras.clear()

        self.leer_rssi_serial()
        idx_direccion = self.obtener_direccion_por_rssi_maximo()
        angulo = self.calcular_angulo_desde_nodo(idx_direccion)

        self.ax_radar.set_title("Radar - Dirección del objetivo")
        self.ax_radar.set_theta_zero_location('N')
        self.ax_radar.set_theta_direction(-1)
        self.ax_radar.set_rticks([])

        angulos = [np.deg2rad(i * 45) for i in range(8)]
        etiquetas = [f"R{i+1}" for i in range(8)]
        self.ax_radar.set_xticks(angulos)
        for angle, label in zip(angulos, etiquetas):
            self.ax_radar.text(angle, 1.05, label, color='black', ha='center', va='center', fontsize=10)

        self.ax_radar.plot([angulo, angulo], [0, 1], color='yellow', linewidth=2)

        self.ax_barras.set_title("RSSI por Nodo")
        self.ax_barras.set_ylim(-100, 0)
        self.ax_barras.set_xticks(np.arange(self.num_nodos))
        self.ax_barras.set_xticklabels([f"R{i+1}" for i in range(self.num_nodos)])
        self.ax_barras.bar(np.arange(self.num_nodos), self.magnitudes_rssi, color='skyblue')

    def iniciar_animacion(self):
        self.anim = FuncAnimation(self.fig, self.actualizar, interval=1000)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    simulador = SimuladorTrilateracion(puerto='COM8', baudios=9600)
    simulador.iniciar_animacion()
