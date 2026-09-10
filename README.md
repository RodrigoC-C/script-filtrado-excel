# SCRIPT PARA EXCEL SISTEMA (FME - FOREIGN MATERIAL EXCLUSION) 

### Descripcion
Este programa fue diseñado para apoyar las funciones de gestion de herramientas en una zona FME, en el cual se busca mantener el sistema de papel, pero luego escanear las hojas diseñas con un respectivo formato para luego pasarlo a sistema y que este se almacene en un excel. 

 1. Existen dos formas de ingresar la data al excel. 
    - La primera opcion es obteniendo el excel que entrega el formulario de microsoft form 
    - La segunda forma es a travez de un json estandarizado para la ingesta masiva de herramientas almacenadas en el contron FME (FOREIGN MATERIAL EXCLUSION).

Todo esto se almacena dentro de dos hojas en excel una de historial donde se registran todas las entradas y otra hoja llamada stock, donde se agrupan todas estas herramientas tanto con su salida como con su entrada, para llevar un calculo de cuantas herramientas se llevan dentro del sistema FME.


## 1. Crear un entorno virtual nuevo y limpio
python -m venv .venv

## 2. Activar el entorno virtual
source .venv/bin/activate  # En Mac/Linux
.venv\Scripts\activate     # En Windows

## 3. Instalar todas las dependencias guardadas
pip install -r requirements.txt


## 4. Cambiar variables de entorno 
Editar el archivo .env.example 

## 5. Correr el archivo main
python main.py

## 6. Pruebas unitarias
Se crearon pruebas unitarias para funciones relevantes de ingesta de informacion con el nombre de test_extraccion.py y test_vulnerabilidad.py