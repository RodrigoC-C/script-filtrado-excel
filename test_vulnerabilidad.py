import unittest
import pandas as pd
import json
import os
from procesamiento import transformacion_entrada_salida

class TestVulnerabilidadesSistema(unittest.TestCase):

    def setUp(self):
        # Preparamos el terreno: un JSON con un error de sintaxis común y un Excel en blanco
        self.json_roto = "test_roto.json"
        with open(self.json_roto, 'w', encoding='utf-8') as f:
            f.write('[{"Herramienta": "pala", "Cantidad": 1},]') # Coma extra al final

        self.excel_temp = "test_maestro.xlsx"
        pd.DataFrame(columns=['Nombre Herramienta', 'Empresa', 'Cantidad']).to_excel(self.excel_temp, index=False)

    def tearDown(self):
        # Limpiamos la basura después de las pruebas
        if os.path.exists(self.json_roto):
            os.remove(self.json_roto)
        if os.path.exists(self.excel_temp):
            os.remove(self.excel_temp)

    # 1. LA TRAMPA MATEMÁTICA: El sistema DEBERÍA manejar texto inválido sin colapsar
    def test_transformacion_texto_en_vez_de_numero(self):
        lista_corrupta = [['cincel', 'dos', '07:30']] # Alguien escribió 'dos'
        
        # IDEALMENTE: El sistema debería terminar el proceso.
        # ACTUALMENTE: Tu código colapsará aquí con un ValueError porque intenta hacer int('dos').
        with self.assertRaises(SystemExit):
            transformacion_entrada_salida(lista_corrupta)

    # 2. LA REBELIÓN DEL JSON: El sistema DEBERÍA rechazar archivos mal formados
    def test_json_mal_formado_coma_extra(self):
        # En tu Opción 2 actual, un JSON mal formateado crashea todo el menú.
        # Esta prueba confirma que la lectura de un JSON roto efectivamente levanta un error crítico.
        with self.assertRaises(json.decoder.JSONDecodeError):
            with open(self.json_roto, 'r', encoding='utf-8') as archivo:
                json.load(archivo)

    # 3. LA AGRUPACIÓN FANTASMA: El sistema DEBERÍA soportar un historial en blanco el día 1
    def test_agrupacion_dataframe_vacio(self):
        # Leemos un historial sin datos, solo con los encabezados
        df_vacio = pd.DataFrame(columns=['Nombre Herramienta', 'Empresa', 'Cantidad'])
        
        try:
            # Replicamos tu línea exacta del main.py
            df_stock = df_vacio.groupby(['Nombre Herramienta','Empresa'], as_index=False)['Cantidad'].sum()
            # Si Pandas lo maneja bien, debería devolver otro DataFrame vacío
            self.assertTrue(df_stock.empty)
        except Exception as e:
            self.fail(f"El sistema colapsó al agrupar un DataFrame vacío. Error: {e}")

if __name__ == '__main__':
    unittest.main()