import os
import re
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Procesamiento de archivos TXT (para generar la tabla) ---
carpeta = "C:/Users/wdg10/Desktop/DirectionFinding-Ordenado/Proceso Secuencial para generar Tablas y graficos RESULTADOS/Mediciones Escenario-Campo Direction Findig"  # ← ¡Reemplaza con tu ruta!
resultados = []
archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt") and "prueba" not in f.lower()]

for archivo in archivos:
    path = os.path.join(carpeta, archivo)
    rssi_vals = []
    
    with open(path, "r") as f:
        for linea in f:
            match = re.search(r"R\d+:\s*(-?\d+\.?\d*)", linea)
            if match:
                rssi_vals.append(float(match.group(1)))
            if len(rssi_vals) >= 45:
                break
    
    if rssi_vals:
        resultados.append({
            "Archivo": archivo.replace(".txt", ""),
            "Promedio (dBm)": round(statistics.mean(rssi_vals), 2),
            "Mínimo (dBm)": min(rssi_vals),
            "Máximo (dBm)": max(rssi_vals),
            "Desviación estándar (dBm)": round(statistics.stdev(rssi_vals), 2),
            "Muestras": len(rssi_vals)
        })

df_resultados = pd.DataFrame(resultados).sort_values("Archivo")

# --- 2. Gráfico Polar con 8 direcciones (NE, NO, SE, SO) ---
# Mapeo de direcciones a ángulos (en grados)
direcciones_angulos = {
    "Norte": 0,
    "Norte-Este": 45,
    "Este": 90,
    "Sur-Este": 135,
    "Sur": 180,
    "Sur-Oeste": 225,
    "Oeste": 270,
    "Norte-Oeste": 315
}

# Extraer dirección y distancia del nombre del archivo
df_resultados["Dirección"] = df_resultados["Archivo"].str.extract(r"([A-Za-z]+-[A-Za-z]+|[A-Za-z]+)(?=-)")
df_resultados["Distancia"] = df_resultados["Archivo"].str.extract(r"(\d+)m").astype(float)

# Convertir ángulos a radianes
df_resultados["Ángulo"] = df_resultados["Dirección"].map(lambda x: np.deg2rad(direcciones_angulos.get(x, np.nan)))
df_resultados = df_resultados.dropna(subset=["Ángulo", "Distancia"])

# Preparar datos para el gráfico
distancias = [4, 8]
valores = {dist: [] for dist in distancias}
angulos_rad = []

for dir in direcciones_angulos:
    if dir in df_resultados["Dirección"].values:
        angulos_rad.append(np.deg2rad(direcciones_angulos[dir]))
        for dist in distancias:
            valor = df_resultados[(df_resultados["Dirección"] == dir) & (df_resultados["Distancia"] == dist)]["Promedio (dBm)"]
            valores[dist].append(-valor.values[0] if not valor.empty else np.nan)

# Cerrar el polígono (conectar último punto con el primero)
angulos_rad.append(angulos_rad[0])
for dist in distancias:
    valores[dist].append(valores[dist][0])

# Crear gráfico
plt.figure(figsize=(10, 8))
ax = plt.subplot(111, polar=True)
colors = ['#1f77b4', '#ff7f0e']  # Azul y naranja

for i, dist in enumerate(distancias):
    ax.plot(angulos_rad, valores[dist], marker='o', color=colors[i], label=f'{dist} metros')
    ax.fill(angulos_rad, valores[dist], color=colors[i], alpha=0.1)

# Ajustes estéticos
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks(angulos_rad[:-1])
ax.set_xticklabels(direcciones_angulos.keys())
ax.set_title("Patrón de RSSI por dirección y distancia", pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()

# Mostrar resultados
print("Tabla de resultados:")
print(df_resultados)
plt.show()
