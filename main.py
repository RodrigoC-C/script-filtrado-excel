# This is script for trasnlater and formting text of form to database of the tools on zone FME of Generation-V4
import os
import pandas as pd 
import json
from openpyxl import load_workbook
from datetime import datetime as dt
from dotenv import load_dotenv
from extraccion import extraccion_herramientas
from procesamiento import transformacion_entrada_salida

# Cargamos las variables de entorno
load_dotenv()

# VARIABLE DE ENTORNOS
archivo_guardado_id = os.getenv("ARCHIVO_GUARDADO_ID")
excel_analizar = os.getenv("EXCEL_PATH")
excel_maestro = os.getenv("EXCEL_MAESTRO_PATH")
hoja_auditoria_maestro = os.getenv("HOJA_MAESTRO_AUDITORIA")

#------------------- Lectura MD registro ---------------------------------------------------------------

# Funcion de lectura del ultimo registro
def lectura_ultimo_registro(nombre_archivo) -> int: 
    # Si el archivo no existe (primera ejecución), devolvemos 0 
    if not os.path.exists(nombre_archivo):
        return 0
    # Leer solo las última línea del archivo Markdown
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.read()
        
    # Separamos por puntos y limpiamos espacios vacíos de forma segura
    registros = [r.strip() for r in lineas.split('.') if r.strip()]

    # Si el archivo está completamente vacío, evitamos que rompa el programa
    if not registros:
        return 0
    
    # Obtener la ultima linea recorrida
    ultimos_registro = registros[-1]

    # Separa id de fecha
    parte_registro = ultimos_registro.split(',')

    ultimo_id = int(parte_registro[0])

    return(ultimo_id)

# Funcion para anotar la ultima lectura del archivo id
def escritura_ultimo_registro(nombre_archivo, id_recorrido, fecha_exacta):

    # Formato para escribir al final de la linea
    guardado_de_id = f"{id_recorrido},{fecha_exacta}."
    with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
        archivo.write(guardado_de_id)
    
    return()


# ------------------ Abrir y cerrar un excel maestro  -----------------------------------------
def abrir_excel(ruta_archivo):
    # Abre excel en modo escritura
    excel_archivo = load_workbook(filename=ruta_archivo)
    return excel_archivo


def escribir_en_hoja_historial(excel_archivo, nombre_hoja, lista_diccionario):
    # Escribe un valor en una celda y hoja específicas.
    hoja = excel_archivo[nombre_hoja]
    # Recorres tu lista de diccionarios
    for movimiento in lista_diccionario:
        # Extraes los valores en el orden EXACTO de tus columnas de Excel
        fila_a_escribir = [
            movimiento['Fecha Entrada/Salida'],
            movimiento['Hora Entrada/Salida'],
            movimiento['Nombre Herramienta'],
            movimiento['Entrada/Salida'],
            movimiento['Cantidad'],
            movimiento['Empresa'],
            movimiento['Persona (Opcional)']
        ]
        
        # append() busca automáticamente la primera fila vacía al final y escribe los datos
        hoja.append(fila_a_escribir)

    return excel_archivo

def guardar_y_cerrar(excel_archivo, ruta_archivo):
    # Guarda los cambios y cierra el archivo liberando memoria. 
    excel_archivo.save(ruta_archivo)
    excel_archivo.close()
    print("Archivo guardado y cerrado exitosamente.")

def recrear_hoja_stock(excel_archivo, nombre_hoja='Stock Actual'):
    # 1. Si la hoja YA EXISTE, mantenemos el formato y solo borramos los datos
    if nombre_hoja in excel_archivo.sheetnames:
        hoja = excel_archivo[nombre_hoja]
        
        # Verificamos que tenga datos debajo de los encabezados
        if hoja.max_row > 1:
            # Borramos desde la fila 2 hasta la última fila existente
            hoja.delete_rows(2, hoja.max_row)
            
    # 2. Si la hoja NO EXISTE (ej. primera ejecución), la creamos
    else:
        hoja = excel_archivo.create_sheet(title=nombre_hoja)
        # Agregamos los encabezados por defecto
        hoja.append(['Nombre Herramienta', 'Empresa', 'Cantidad Total'])
    
    return hoja

# ------------------------ Main -------------------------------------

print("--- SISTEMA DE INVENTARIO ---")
print("1. Ingresar nuevos registros desde Formulario (Excel)")
print("2. Ingreso Masivo desde Escaneo (JSON)")
    
opcion = input("Ingresa el número de tu opción (1 o 2): ").strip()

# Donde guardaremos todos los diccionarios
lista_diccionario = []

if opcion == '1':
    # Ultimo id 
    id_recorrido = lectura_ultimo_registro(archivo_guardado_id)

    # Lectura del excel
    df = pd.read_excel(excel_analizar)

    # Busqueda de ultimo id 
    ultimo_id = df[df['ID'] == id_recorrido].index
    print(ultimo_id)

    if not ultimo_id.empty:
        indice = ultimo_id[0]
        # Cortamos la tabla usando iloc: desde la fila siguiente (+1) hasta el final
        df_nuevos = df.iloc[indice + 1:]
        print(df_nuevos)

    else:
        # Si no encontramos el ID. Puede ser la primera vez (ID 0) o no hay nada nuevo.
        if id_recorrido == 0:
            df_nuevos = df # Procesamos todo porque es la primera ejecución
        else:
            # Creamos una tabla vacía para que el código sepa que no debe hacer nada
            df_nuevos = pd.DataFrame(columns=df.columns)

    id_actual = id_recorrido
    # 4. El Bucle: Recorremos solo las filas nuevas
    # iterrows() avanza fila por fila manteniendo el "apuntador" automáticamente
    for index, fila in df_nuevos.iterrows():

        # Extraes las variables específicas de esta fila
        id_actual = fila['ID']
        entrada_salida = fila['Entrada o Salida']
        fecha_ingreso = fila.iloc[7]
        empresa = fila['Empresa Responsable de la Herramienta']
        persona = fila['Nombre de Persona que ingresa las Herramientas'] # Esta variable puede mantenerse nulo es opcional
        herramientas = fila.iloc[10]

        # Extraemos las herramientas para iterarla de texto a listas
        herramientas_lista = extraccion_herramientas(herramientas)

        if entrada_salida == "Salida":
            transformacion_entrada_salida(herramientas_lista)
        else: 
            entrada_salida = entrada_salida

        for item in herramientas_lista: 
            diccionario_herramientas = {
                "Fecha Entrada/Salida": fecha_ingreso.strftime("%d/%m/%Y") if pd.notnull(fecha_ingreso) else None,
                "Hora Entrada/Salida":item[2] if item[2] else None,
                "Nombre Herramienta": item[0],
                "Entrada/Salida": entrada_salida,
                "Cantidad": item[1],
                "Empresa": empresa,
                "Persona (Opcional)": persona if pd.notnull(persona) else None
            }  
            # Por cada herramienta creamos un diccionario y lo mandamos agregamos a herramientas 
            lista_diccionario.append(diccionario_herramientas)

    # 4. SOLO guardamos un nuevo ID en el MD si realmente procesamos filas nuevas
    if not df_nuevos.empty:
        # Extraemos el último ID directamente de la columna para evitar errores con filas en blanco
        ultimo_id_valido = int(df_nuevos['ID'].dropna().iloc[-1])
        
        # Darle un formato limpio (Día/Mes/Año Hora:Minuto:Segundo)
        fecha_exacta = dt.now().strftime("%d/%m/%Y %H:%M")
        
        # Guardamos el ID final
        escritura_ultimo_registro(archivo_guardado_id, ultimo_id_valido, fecha_exacta)
        print(f"Registro MD actualizado con éxito. Último ID: {ultimo_id_valido}")
    else:
        print("No hay registros nuevos en el formulario. El inventario está al día.")



elif opcion == '2':
    print("Iniciando ingreso masivo por JSON...")
    ruta_json = 'ingreso_masivo.json'
    
    if not os.path.exists(ruta_json):
        print(f"⚠️ Error: No se encontró el archivo '{ruta_json}'.")
    else:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)
            
        for item in datos_json:
            # Extracción y limpieza segura
            cantidad = int(item.get('Cantidad', 0))
            movimiento = item.get('Movimiento', 'Entrada')
            
            # Lógica matemática para salidas
            if movimiento.lower() == 'salida':
                cantidad = cantidad * -1
                
            diccionario_herramientas = {
                "Fecha Entrada/Salida": item.get('Fecha_Ingreso', dt.now().strftime("%d/%m/%Y")),
                "Hora Entrada/Salida": item.get('Hora_Entrada/Salida').strip().title(), 
                "Nombre Herramienta": str(item.get('Herramienta', '')).strip().title(),
                "Entrada/Salida": movimiento.capitalize(),
                "Cantidad": cantidad,
                "Empresa": str(item.get('Empresa', '')).strip().title(),
                "Persona (Opcional)": item.get('Responsable', None)
            }
            # Se inyecta en la misma caja universal que usa el Excel
            lista_diccionario.append(diccionario_herramientas)


else:
    print("Opción no válida. Ejecuta el script de nuevo.")
    
# ------------------------------------------------------------------------------------------------------

# Abrimos el excel para su escritura
abrir_excel_maestro = abrir_excel(excel_maestro)

# Realizamos el guardado de cada diccionario en la hoja de auditoria 
excel_modificado = escribir_en_hoja_historial(abrir_excel_maestro, hoja_auditoria_maestro, lista_diccionario)
guardar_y_cerrar(excel_modificado, excel_maestro)


# ------------------------ Agrupacion y creacion de hoja stock ----------------------------------------
# Leemos la hoja completa de historial
df_maestro_historial = pd.read_excel(excel_maestro, sheet_name='Historial')

# Realizamos la agrupacion por nombre y sumamos la cantidad
df_stock = df_maestro_historial.groupby(['Nombre Herramienta','Empresa'], as_index=False)['Cantidad'].sum()

# Abrimos el excel para su escritura
abrir_excel_maestro = abrir_excel(excel_maestro)


# realizamos la eliminacion de la antigua hoja para empezar de 0
hoja_stock_nueva = recrear_hoja_stock(abrir_excel_maestro, 'Stock Actual')

for index, fila in df_stock.iterrows():
    # Armamos una lista simple con los datos de esta fila exacta
    fila_a_escribir = [
        fila['Nombre Herramienta'], 
        fila['Empresa'], 
        fila['Cantidad']
    ]
    # Escribimos la lista en la nueva hoja
    hoja_stock_nueva.append(fila_a_escribir)

guardar_y_cerrar(abrir_excel_maestro, excel_maestro)