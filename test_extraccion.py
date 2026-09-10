import unittest
# Asumiendo que tu función está en extraccion.py
from extraccion import extraccion_herramientas 

class TestExtraccionHerramientas(unittest.TestCase):

    def test_formato_ideal(self):
        # El usuario hace todo bien
        resultado = extraccion_herramientas("cincel, 2, 07:30.")
        self.assertEqual(resultado, [['cincel', '2', '07:30']])

    def test_falta_hora_sin_coma(self):
        # El usuario olvida la hora y la última coma
        resultado = extraccion_herramientas("martillo, 5.")
        self.assertEqual(resultado, [['martillo', '5', None]])

    def test_falta_hora_con_coma_vacia(self):
        # El usuario pone la coma pero deja el espacio vacío (tu dilema actual)
        resultado = extraccion_herramientas("taladro, 1, .")
        self.assertEqual(resultado, [['taladro', '1', None]])

    def test_multiples_herramientas_desordenadas(self):
        # El usuario mezcla formatos en una sola respuesta
        texto = "sierra, 2, 08:00. pala, 3. alicate, 1, ."
        resultado = extraccion_herramientas(texto)
        esperado = [
            ['sierra', '2', '08:00'],
            ['pala', '3', None],
            ['alicate', '1', None]
        ]
        self.assertEqual(resultado, esperado)

    def test_celda_vacia_o_nula(self):
        # El usuario deja la celda en blanco (Pandas envía NaN o None)
        self.assertEqual(extraccion_herramientas(None), [])
        self.assertEqual(extraccion_herramientas("   "), [])

if __name__ == '__main__':
    unittest.main()