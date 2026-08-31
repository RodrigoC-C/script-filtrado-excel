# This is script for trasnlater and formting text of form to database of the tools on zone FME of Generation-V4
import os
import pandas as pd 
from datetime import datetime as dt
from dotenv import load_dotenv
from extraccion import extraccion_herramientas

# Cargamos las variables de entorno
load_dotenv()

# VARIABLE DE ENTORNOS
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


def guardar_herramientas(herramienta, cantidad, hora):

    return()


# Ultimo id 
id_recorrido = lectura_ultimo_registro(archivo_guardado_id)
# + 1 para el id siguiente

# Lectura del excel
df = pd.read_excel(excel_analizar)

# Busqueda de ultimo id 
ultimo_id = df[df['ID'] == id_recorrido].index

print(ultimo_id)

if not ultimo_id.empty:
    indice = ultimo_id[0]
    # Cortamos la tabla usando iloc: desde la fila siguiente (+1) hasta el final
    df_nuevos = df.iloc[indice:]
    print("test 1")
    print(df_nuevos)
else:
    # Si el ID no existe (ej. se borró o es tu primera vez corriendo el script), procesamos todo
    df_nuevos = df

# 4. El Bucle: Recorremos solo las filas nuevas (reemplaza al While)
# iterrows() avanza fila por fila manteniendo el "apuntador" automáticamente
for index, fila in df_nuevos.iterrows():
    
    # Extraes las variables específicas de esta fila
    id_actual = fila['ID']
    entrada_salida = fila['Entrada o Salida']
    fecha_ingreso = fila['''Ingrese fecha 
''']
    empresa = fila['Empresa Responsable de la Herramienta']
    persona = fila['Nombre de Persona que ingresa las Herramientas'] # Esta variable puede mantenerse nulo es opcional
    herramientas = fila['''Ingrese las Herramientas con el siguiente formato: 

Formato: [nombre herramienta, cantidad de herramienta, hora de registro.] 

Ejemplo: cincel, 2, 07:30.                                         ...''']
    
    # Aquí es donde llamas a tu función personalizada
    # resultado = mi_funcion_procesadora(id_actual, variable_a, variable_b)
    
    print(f"Procesando nuevo registro: {id_actual}, {entrada_salida}, {fecha_ingreso}, {empresa}, {persona}, {herramientas}")

    extraccion_herramientas(herramientas)

# Capturar el momento exacto de la ejecución
ahora = dt.now()
# Darle un formato limpio (Día/Mes/Año Hora:Minuto:Segundo)
fecha_exacta = ahora.strftime("%d/%m/%Y %H:%M")

# Id recorrido sumandole 1 (aca se asignara el ultimo registro analizado
id_recorrido = id_recorrido
# Ultimo Id que se deja registro en el archivo para no caer en rebundancia
#escritura_ultimo_registro(archivo_guardado_id, id_recorrido, fecha_exacta)