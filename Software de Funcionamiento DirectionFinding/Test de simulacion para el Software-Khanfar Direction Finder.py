import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class SimuladorTrilateracion:
    def __init__(self):
        self.num_nodos = 8
        self.lado = 10.0
        self.posiciones_nodos = self.generar_posiciones_nodos()
        self.magnitudes_rssi = np.random.randint(-90, -30, size=self.num_nodos).astype(float)
        self.fig = plt.figure(figsize=(10, 5))
        self.ax_radar = self.fig.add_subplot(1, 2, 1, polar=True)
        self.ax_barras = self.fig.add_subplot(1, 2, 2)
        self.anim = None

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

    def convertir_rssi_a_distancia(self, rssi):
        A = -50
        n = 2.0
        return 10 ** ((A - rssi) / (10 * n))

    def estimar_posicion(self):
        indices_validos = self.magnitudes_rssi > -99
        posiciones_validas = self.posiciones_nodos[indices_validos]
        rssi_validos = self.magnitudes_rssi[indices_validos]

        if len(posiciones_validas) < 3:
            return np.array([-1, -1])

        distancias = self.convertir_rssi_a_distancia(rssi_validos)
        pesos = 1 / (distancias + 1e-6)
        pesos /= np.sum(pesos)
        return np.average(posiciones_validas, axis=0, weights=pesos)

    def calcular_angulo(self, posicion):
        dx = posicion[0] - self.lado / 2
        dy = posicion[1] - self.lado / 2
        angulo = np.arctan2(dy, dx)
        return angulo if angulo >= 0 else (2 * np.pi + angulo)

    def actualizar(self, frame):
        self.ax_radar.clear()
        self.ax_barras.clear()

        # Simulación de cambios aleatorios en RSSI
        self.magnitudes_rssi = np.random.randint(-90, -30, size=self.num_nodos).astype(float)
        estimacion = self.estimar_posicion()

        # Radar
        self.ax_radar.set_title("Radar - Dirección del objetivo")
        self.ax_radar.set_theta_zero_location('N')
        self.ax_radar.set_theta_direction(-1)
        self.ax_radar.set_rticks([])
        self.ax_radar.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4])
        self.ax_radar.set_xticklabels(['N', '45°', 'E', '135°', 'S', '225°', 'W', '315°'])

        # Dibujar línea si hay estimación
        if estimacion[0] >= 0:
            angulo = self.calcular_angulo(estimacion)
            self.ax_radar.plot([angulo, angulo], [0, 1], color='yellow', linewidth=2)
        else:
            self.ax_radar.text(0, 0, "Esperando datos...", color='red', ha='center')

        # Barras de RSSI
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
    simulador = SimuladorTrilateracion()
    simulador.iniciar_animacion()

