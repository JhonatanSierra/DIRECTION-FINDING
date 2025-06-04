import os
import pandas as pd

# Ruta del archivo Excel
ruta_excel = r"C:\Users\wdg10\Desktop\Tablas Resultados\DATARAW-Mediciones.xlsx"

# Carpeta de salida para los archivos CSV
carpeta_base = r"C:\Users\wdg10\Desktop\Tablas Resultados"
carpeta_salida = os.path.join(carpeta_base, "CSV_Salidas")

# Crear la carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Leer todas las hojas del Excel
excel = pd.ExcelFile(ruta_excel)
nombres_hojas = excel.sheet_names

# Procesar y guardar cada hoja como archivo CSV
for hoja in nombres_hojas:
    df = excel.parse(hoja)
    nombre_archivo = f"{hoja}.csv"
    ruta_csv = os.path.join(carpeta_salida, nombre_archivo)
    df.to_csv(ruta_csv, index=False, sep=",")
    print(f"✅ Archivo guardado: {ruta_csv}")
