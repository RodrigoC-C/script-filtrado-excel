import pandas as pd
# Lectura de casillas y extraccion de variables de herramientas
def extraccion_herramientas(herramienta):
    # Escudo contra celdas vacías o valores NaN de Pandas
    if pd.isna(herramienta) or not str(herramienta).strip():
        return []
    # Pasamos todo el texto en minuscula
    texto_minuscula = herramienta.lower()

    pasadas = [p.strip() for p in texto_minuscula.split('.') if p.strip()] # Compresion de lista en python, es primera vez que lo veo
    lista_anidada = [] # para guardar la lista y luego iterar sobre ella

    for i, pasada in enumerate(pasadas, start=1): # enumarate es para ahorrarse el 1 a fuera del bucle, ya que este se asigna en i
        elementos = [item.strip() if item.strip() else None for item in pasada.split(',')] # volvemos a ocupar compresion de lista pero para cortar los item y eliminar espacios

        # Escudo contra falta de datos (ej: escribieron "cincel, 2" sin hora)
        # Mientras la lista tenga menos de 3 elementos, la rellenamos con None
        while len(elementos) < 3:
            elementos.append(None)

        lista_anidada.append(elementos)
    
    return lista_anidada