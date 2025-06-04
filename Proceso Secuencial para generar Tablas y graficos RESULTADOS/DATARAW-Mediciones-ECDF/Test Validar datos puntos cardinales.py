archivo = r"C:\Users\wdg10\Desktop\Tablas Resultados\CSV_Salidas\Este-4m.csv"

with open(archivo, "r", encoding="utf-8") as f:
    for i, linea in enumerate(f):
        print(f"Línea {i+1}: {repr(linea)}")
        if i >= 4:
            break
