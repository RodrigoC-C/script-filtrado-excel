# Lectura de casillas y extraccion de variables de herramientas
def extraccion_herramientas(herramienta):
    # Pasamos todo el texto en minuscula
    texto_minuscula = herramienta.lower()

    pasadas = [p.strip() for p in texto_minuscula.split('.') if p.strip()] # Compresion de lista en python, es primera vez que lo veo

    for i, pasada in enumerate(pasadas, start=1): # enumarate es para ahorrarse el 1 a fuera del bucle, ya que este se asigna en i
        elementos = [item.strip() for item in pasada.split(',')] # volvemos a ocupar compresion de lista pero para cortar los item y eliminar espacios
        print(f"Pasada {i}: {elementos}")
    
    return()