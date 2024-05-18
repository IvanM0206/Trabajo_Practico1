from matricesRalas import MatrizRala
import math

# Funcion para calcular la norma


def norma(vector: MatrizRala) -> float:
    res: float = 0
    for fila in vector.filas.values():
        res += (fila.raiz.valor[1]) ** 2

    return math.sqrt(res)
