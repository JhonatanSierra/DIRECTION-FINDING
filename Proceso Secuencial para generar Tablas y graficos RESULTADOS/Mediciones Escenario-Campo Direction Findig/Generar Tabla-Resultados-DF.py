import os
import re
import statistics
import pandas as pd

# Ruta donde están los archivos TXT
carpeta = "C:/Users/wdg10/Desktop/DirectionFinding-Ordenado/Proceso Secuencial para generar Tablas y graficos RESULTADOS/Mediciones Escenario-Campo Direction Findig"  # ← Reemplaza esto con tu ruta local

# Preparar resultados
resultados = []

# Filtrar los archivos .txt válidos
archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt") and "prueba" not in f.lower()]

for archivo in archivos:
    path = os.path.join(carpeta, archivo)
    rssi_vals = []

    with open(path, "r") as f:
        for linea in f:
            match = re.search(r"R\d+:\s*(-?\d+\.?\d*)", linea)
            if match:
                rssi_vals.append(float(match.group(1)))
            if len(rssi_vals) >= 20:
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

# Mostrar los resultados en forma de tabla
df_resultados = pd.DataFrame(resultados)
print(df_resultados.sort_values("Archivo"))
