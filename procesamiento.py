# Analizar si dentro de la hoja stock se tiene las herramientas para hacer el procesamiento



# Transformar de entrada y salida a positivo o negativo
def transformacion_entrada_salida(herramientas_lista):
    herramientas_lista_nueva = []
    for item in herramientas_lista:
        item[1] = int(item[1]) * -1 # transformamos el item a numero para poder pasarlo a negativo
        herramientas_lista_nueva.append(item)

    return herramientas_lista_nueva
     