from typing import List
from matricesRalas import MatrizRala

def GaussJordan(A, b):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    # Chequear que el tamaño de b sea correcto. Chequear al inicio si b tiene alguna posicion que no es 0 y en A esa fila es todo 0's

    cantPivotes = min(A.shape[0], A.shape[1])
    matriz_temp_gj = A
    pos_pivotes_usados: List[int] = []
    pivote = None
    pos_columna_pivote = None

    for pos_fila_pivotes in range(cantPivotes):
        #print(matriz_temp_gj)
        if pos_fila_pivotes not in matriz_temp_gj.filas.keys():
            if b[pos_fila_pivotes, 0] != 0:
                raise ArithmeticError("El sistema no tiene solucion")
        else:
            nodo = matriz_temp_gj.filas[pos_fila_pivotes].raiz
            encontrado = False
            while nodo is not None and not encontrado:
                if nodo.valor[0] not in pos_pivotes_usados:
                    encontrado = True
                    pos_pivotes_usados.append(nodo.valor[0])
                    pos_columna_pivote = nodo.valor[0]
                    pivote = A[pos_fila_pivotes, pos_columna_pivote]

                nodo = nodo.siguiente

            #print("pivote", pivote)

            if pivote != 1:
                nodo = matriz_temp_gj.filas[pos_fila_pivotes].raiz
                while nodo is not None:
                    #print("pos", nodo.valor)
                    matriz_temp_gj[pos_fila_pivotes, nodo.valor[0]] /= pivote
                    nodo = nodo.siguiente

                b[pos_fila_pivotes, 0] /= pivote

            #print("primera", repr(matriz_temp_gj))
            filas_a_restar = list(matriz_temp_gj.filas.keys()).copy()
            filas_a_restar.remove(pos_fila_pivotes)
            for fila in filas_a_restar:
                multiplicador: float = matriz_temp_gj[fila, pos_columna_pivote]
                nodo = matriz_temp_gj.filas[pos_fila_pivotes].raiz
                columna: int = None
                while nodo is not None:
                    columna = nodo.valor[0]
                    matriz_temp_gj[fila, columna] = (
                                matriz_temp_gj[fila, columna]
                                - multiplicador
                                * nodo.valor[1]
                                )
                    nodo = nodo.siguiente

                b[fila, 0] = b[fila, 0] - b[pos_fila_pivotes, 0] * multiplicador


    res = MatrizRala(A.shape[1], 1)

    #print(repr(matriz_temp_gj), repr(b))

    filas = set([x for x in range(A.shape[0])])
    filas_restantes = filas - set(matriz_temp_gj.filas.keys())
    #print(filas, filas_restantes)

    for nro_fila in filas_restantes:
        if b[nro_fila, 0] != 0:
            raise ArithmeticError("El sistema no tiene solucion")
    
    if len(matriz_temp_gj.filas.keys()) != A.shape[1]:
        raise ArithmeticError("El sistema tiene infinitas soluciones")

    for nro_fila, fila in matriz_temp_gj.filas.items():
        for nodo in fila:
            # print(nodo)
            if nodo[1] != 0:
                res[nodo[0], 0] = b[nro_fila, 0]

    return res


""" sol_unica = True
    pos_error = None
    for pos_pivotes in range(cantPivotes):
        if matriz_temp_gj[pos_pivotes, pos_pivotes] == 0:
            sol_unica = False
            pos_error = pos_pivotes

    if not sol_unica:
        if b[pos_error, 0] != 0:
            raise ArithmeticError("El sistema no tiene solucion")
        else:
            raise ArithmeticError("El sistema tiene infinitas soluciones")"""

""""
    
    if matriz_temp_gj.shape[0] < A.shape[0]:
        raise ArithmeticError("El sistema tiene infinitas soluciones")
    else:
        for fila in matriz_temp_gj.filas.values():
            if len(fila) == 1 and fila.raiz[0] == A.shape[0]+1:
                raise ArithmeticError("El sistema no tiene solucion")
            else:
                ultimoNodo = fila.nodoPorCondicion(lambda nodo_temp: nodo_temp.siguiente is None)
                res.append(ultimoNodo[1])"""