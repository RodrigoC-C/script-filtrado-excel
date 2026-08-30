# script-filtrado-excel

# 1. Crear un entorno virtual nuevo y limpio
python -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate  # En Mac/Linux
.venv\Scripts\activate     # En Windows

# 3. Instalar todas las dependencias guardadas
pip install -r requirements.txt


# 4. Cambiar variables de entorno 
Editar el archivo .env.example 

# 5. Correr el archivo main
python main.py