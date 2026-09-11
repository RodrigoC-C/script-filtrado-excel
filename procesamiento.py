import sys
import pandas as pd
# Transformar de entrada y salida a positivo o negativo
def transformacion_entrada_salida(herramientas_lista):
    herramientas_lista_nueva = []
    for item in herramientas_lista:
        try: 
            item[1] = int(item[1]) * -1 # transformamos el item a numero para poder pasarlo a negativo
            herramientas_lista_nueva.append(item)
        except ValueError:
            # Imprime un mensaje claro y detiene la ejecución en seco
            print(f"\n🛑 ERROR FATAL: La cantidad '{item[1]}' en la herramienta '{item[0]}' no es un número.")
            print("El programa se ha detenido para proteger la base de datos.")
            print("Corrige el error en tu Excel o JSON y vuelve a ejecutar.")
            sys.exit(1)

    return herramientas_lista_nueva

def formatear_herramienta(texto):
    if pd.isna(texto) or not str(texto).strip():
        return None
    return str(texto).strip().lower()

def formatear_empresa(texto):
    if pd.isna(texto) or not str(texto).strip():
        return None
    return str(texto).strip().upper()

def formatear_persona(texto):
    if pd.isna(texto) or not str(texto).strip():
        return None
    return str(texto).strip().title()

def formatear_movimiento(texto):
    if pd.isna(texto) or not str(texto).strip():
        return "Entrada" # Por defecto asumimos entrada si viene vacío
    return str(texto).strip().capitalize()
     