import os
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
carpeta_csv = r"C:\Users\wdg10\Desktop\Tablas Resultados\CSV_Salidas"
carpeta_salida = os.path.join(carpeta_csv, "Analisis_Resultados")
os.makedirs(carpeta_salida, exist_ok=True)

# === Procesar todos los archivos .csv ===
archivos_csv = [f for f in os.listdir(carpeta_csv) if f.endswith(".csv")]

for archivo in archivos_csv:
    ruta_archivo = os.path.join(carpeta_csv, archivo)
    nombre_base = archivo.replace(".csv", "")

    # Leer archivo
    try:
        df = pd.read_csv(ruta_archivo, header=None, names=["Fecha", "Hora", "Separador", "Nodo", "RSSI"])
    except Exception as e:
        print(f"❌ Error al leer {archivo}: {e}")
        continue

    # Limpiar columnas
    df["Nodo"] = df["Nodo"].str.strip().str.upper().str.replace(":", "")
    df["RSSI"] = pd.to_numeric(df["RSSI"], errors="coerce")

    # Filtrar nodos válidos
    df = df[df["Nodo"].isin([f"R{i}" for i in range(1, 9)])]

    if df.empty:
        print(f"⚠️ Sin datos válidos en {archivo}")
        continue

    muestras_maximas = df["Nodo"].value_counts().max()

    # Análisis por nodo
    resultados = []
    for i in range(1, 9):
        nodo = f"R{i}"
        datos = df[df["Nodo"] == nodo]["RSSI"]

        if not datos.empty:
            promedio = round(datos.mean(), 2)
            minimo = datos.min()
            maximo = datos.max()
            desviacion = round(datos.std(), 2)
            cantidad = len(datos)
            efectividad = round((cantidad / muestras_maximas) * 100, 2)
        else:
            promedio = minimo = maximo = desviacion = efectividad = 0
            cantidad = 0

        resultados.append({
            "Nodo transmisor": nodo,
            "Promedio RSSI (dBm)": promedio,
            "Mínimo (dBm)": minimo,
            "Máximo (dBm)": maximo,
            "Desviación Std": desviacion,
            "Muestras": cantidad,
            "% Efectividad": efectividad
        })

    df_resultados = pd.DataFrame(resultados)

    # Guardar tabla
    ruta_csv = os.path.join(carpeta_salida, f"Tabla_{nombre_base}.csv")
    df_resultados.to_csv(ruta_csv, index=False)
    print(f"✅ Tabla guardada: {ruta_csv}")

    # Gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(df_resultados["Nodo transmisor"], df_resultados["Promedio RSSI (dBm)"], color="teal")
    plt.title(f"Gráfica de Cobertura - {nombre_base}")
    plt.ylabel("RSSI Promedio (dBm)")
    plt.ylim(-100, 0)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    ruta_png = os.path.join(carpeta_salida, f"Grafica_{nombre_base}.png")
    plt.savefig(ruta_png)
    plt.close()
    print(f"📈 Gráfica guardada: {ruta_png}")
