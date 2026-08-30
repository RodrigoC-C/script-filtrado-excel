# This is script for trasnlater and formting text of form to database of the tools on zone FME of Generation-V4
import os
import pandas as pd 
from datetime import datetime as dt
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

#VARIABLE DE ENTORNOS
archivo_guardado_id = os.getenv("ARCHIVO_GUARDADO_ID")
excel_analizar = os.getenv("EXCEL_PATH")


# Funcion de lectura del ultimo registro
def lectura_ultimo_registro(nombre_archivo) -> int: 
    # Leer solo las última línea del archivo Markdown
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.read()
        
    # Separamos por puntos y limpiamos espacios vacíos de forma segura
    registros = [r.strip() for r in lineas.split('.') if r.strip()]

    # Si el archivo está completamente vacío, evitamos que rompa el programa
    if not registros:
        raise ValueError(f"⚠️ Error fatal: El archivo '{nombre_archivo}' está vacío o no tiene registros válidos.")
    # Obtener la ultima linea recorrida
    ultimos_registro = registros[-1]

    # Separa id de fecha
    parte_registro = ultimos_registro.split(',')

    ultimo_id = int(parte_registro[0])
    ultima_fecha = parte_registro[1]

    return(ultimo_id)



# Funcion para anotar la ultima lectura del archivo id
def escritura_ultimo_registro(nombre_archivo, id_recorrido, fecha_exacta):

    # Formato para escribir al final de la linea
    guardado_de_id = f"{id_recorrido},{fecha_exacta}."
    with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
        archivo.write(guardado_de_id)
    
    return()





# Ultimo id 
id_recorrido = lectura_ultimo_registro(archivo_guardado_id)
# + 1 para el id siguiente

# Lectura del excel
df = pd.read_excel(excel_analizar)

# Busqueda de ultimo id 
fila = df[df['ID'] == id_recorrido]
 
print(fila)

# Capturar el momento exacto de la ejecución
ahora = dt.now()
# Darle un formato limpio (Día/Mes/Año Hora:Minuto:Segundo)
fecha_exacta = ahora.strftime("%d/%m/%Y %H:%M")

# Id recorrido sumandole 1 (aca se asignara el ultimo registro analizado
id_recorrido = id_recorrido
# Ultimo Id que se deja registro en el archivo para no caer en rebundancia
escritura_ultimo_registro(archivo_guardado_id, id_recorrido, fecha_exacta)