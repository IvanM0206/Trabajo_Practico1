# Iván Mondrzak y Federico Peitti

from typing import List
from matricesRalas import MatrizRala


def GaussJordan(A, b):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    # Chequear que el tamaño de b sea correcto. Chequear al inicio si b tiene alguna posicion que no es 0 y en A esa fila es todo 0's

    cantPivotes = min(A.shape[0], A.shape[1])
    matrizTemporal = A
    pivotesUsados: List[int] = []
    pivote = None
    columnaPivote = None

    # Se itera sobre las filas candidatas
    for filaPivote in range(cantPivotes):
        # Si la fila es 0 pero en b el valor correspondiente es no nulo, el sistema no tiene solución
        if filaPivote not in matrizTemporal.filas.keys():
            if b[filaPivote, 0] != 0:
                raise ArithmeticError("El sistema no tiene solución")

        #
        else:
            nodo = matrizTemporal.filas[filaPivote].raiz
            encontrado = False
            # Buscar el próximo pivote en la fila tal que la columna no tenga ya uno asignado
            while nodo is not None and not encontrado:
                if nodo.valor[0] not in pivotesUsados:
                    encontrado = True
                    pivotesUsados.append(nodo.valor[0])
                    columnaPivote = nodo.valor[0]
                    pivote = A[filaPivote, columnaPivote]

                nodo = nodo.siguiente

            # Normalizar el pivote a 1 (y su fila asociada se divide)
            if pivote != 1:
                nodo = matrizTemporal.filas[filaPivote].raiz
                while nodo is not None:
                    matrizTemporal[filaPivote, nodo.valor[0]] /= pivote
                    nodo = nodo.siguiente

                b[filaPivote, 0] /= pivote

            # Se restan todas las filas menos la del pivote
            filas_a_restar = list(matrizTemporal.filas.keys()).copy()
            filas_a_restar.remove(filaPivote)

            for fila in filas_a_restar:
                # Cada fila se resta por la fila pivote por el multiplicador correspondiente para que
                # la columna del pivote quede en 0 (sólo el pivote queda en 1)
                multiplicador: float = matrizTemporal[fila, columnaPivote]
                nodo = matrizTemporal.filas[filaPivote].raiz
                columna: int = None
                while nodo is not None:
                    columna = nodo.valor[0]
                    matrizTemporal[fila, columna] = (
                        matrizTemporal[fila, columna] - multiplicador * nodo.valor[1]
                    )
                    nodo = nodo.siguiente

                # Mismo proceso para el vector b
                b[fila, 0] = b[fila, 0] - b[filaPivote, 0] * multiplicador

    # Vector resultado
    res = MatrizRala(A.shape[1], 1)

    # Filas restantes sin pivote asignado (filas nulas en caso de haberlas)
    filas = set([x for x in range(A.shape[0])])
    filasRestantes = filas - set(matrizTemporal.filas.keys())

    # Si queda la fila del estilo (0 0 .... 0 | b) con b!= 0, el sistema no tiene solución
    for nro_fila in filasRestantes:
        if b[nro_fila, 0] != 0:
            raise ArithmeticError("El sistema no tiene solución")
    # Caso contrario, el sistema es compatible

    # Si no hay un pivote por variable, el sistema es compatible indeterminado
    if len(matrizTemporal.filas.keys()) != A.shape[1]:
        raise ArithmeticError("El sistema tiene infinitas soluciones")

    # Si hay solución, se reconstruye en res, y basta con mirar al vector b tras hacer Gauss Jordan en la matriz temporal
    for nro_fila, fila in matrizTemporal.filas.items():
        # Notar que los pivotes no necesariamente están ordenados, por lo que b ampliado no es necesariamente el vector resultado en orden
        for nodo in fila:
            if nodo[1] != 0:
                res[nodo[0], 0] = b[nro_fila, 0]

    return res
