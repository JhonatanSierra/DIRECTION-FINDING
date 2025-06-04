import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo_resultado = r"C:\Users\wdg10\Desktop\DirectionFinding-Ordenado\Proceso Secuencial para generar Tablas y graficos RESULTADOS\DATARAW-Mediciones\Analisis_Resultados\Tabla_Este-4m.csv"
nodo_referencia = "R2"  # Cambia esto al nodo que quieras resaltar

# === Leer tabla de resultados ===
df_resultados = pd.read_csv(archivo_resultado)

# Validar que el nodo de referencia exista
if nodo_referencia not in df_resultados["Nodo transmisor"].values:
    print(f"⚠️ El nodo de referencia '{nodo_referencia}' no se encuentra en la tabla.")
else:
    # Ordenar para visualización clara
    df_plot = df_resultados.set_index("Nodo transmisor")["Promedio RSSI (dBm)"].sort_values()

    plt.figure(figsize=(10, 6))
    plt.bar(df_plot.index, df_plot.values, color="skyblue")

    # Línea para el nodo de referencia
    valor_ref = df_resultados[df_resultados["Nodo transmisor"] == nodo_referencia]["Promedio RSSI (dBm)"].values[0]
    plt.axhline(valor_ref, color="red", linestyle="--", label=f"Referencia: {nodo_referencia} ({valor_ref} dBm)")

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("RSSI Promedio (dBm)")
    plt.title(f"Comparación de Cobertura vs Nodo {nodo_referencia}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
