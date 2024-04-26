# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan
from typing import Dict, List

import numpy as np


class ListaEnlazada:
    def __init__(self):
        self.raiz = None
        self.longitud = 0

        self.current = self.Nodo(None, self.raiz)

    def insertarFrente(self, valor):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)

        nuevoNodo = self.Nodo(valor, self.raiz)
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo(self, valor, nodoAnterior):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo(valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push(self, valor):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo(valor, None)
        else:
            nuevoNodo = self.Nodo(valor, None)
            ultimoNodo = self.nodoPorCondicion(lambda n: n.siguiente is None)
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def pop(self):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion(lambda n: n.siguiente.siguiente is None)
            anteUltimoNodo.siguiente = None

        self.longitud -= 1

        return self

    def nodoPorCondicion(self, funcionCondicion):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')

        nodoActual = self.raiz
        while not funcionCondicion(nodoActual):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')

        return nodoActual

    def __len__(self):
        return self.longitud

    def __iter__(self):
        self.current = self.Nodo(None, self.raiz)
        return self

    def __next__(self):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor

    def __repr__(self):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__(self, valor, siguiente):
            self.valor = valor
            self.siguiente = siguiente


class MatrizRala:
    def __init__(self, M, N):
        self.filas: Dict[int, ListaEnlazada[ListaEnlazada.Nodo]] = {}
        self.shape = (M, N)

    def __getitem__(self, Idx):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]

        if Idx[0] >= self.shape[0] or Idx[1] >= self.shape[1]:
            raise IndexError("Esa posicion no existe en la matriz")

        res: int = 0

        if Idx[0] in self.filas.keys():
            for nodo in self.filas[Idx[0]]:
                if nodo[0] == Idx[1]:
                    res = nodo[1]

        return res

    def __setitem__(self, Idx, v):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        if Idx[0] >= self.shape[0] or Idx[1] >= self.shape[1]:
            raise IndexError("Esa posicion no existe en la matriz")

        complete: bool = False

        if v == 0:
            if self[Idx[0], Idx[1]] == 0:
                return self

            else:
                if len(self.filas[Idx[0]]) == 1:
                    self.filas[Idx[0]].pop()
                    self.filas.pop(Idx[0])
                else:
                    nuevaFila: ListaEnlazada = ListaEnlazada()
                    nodoAEliminar = self.filas[Idx[0]].nodoPorCondicion(lambda nodo_temp: nodo_temp.valor[0] == Idx[1])
                    for nodo in self.filas[Idx[0]]:
                        if nodo[0] != nodoAEliminar.valor[0]:
                            nuevaFila.push(nodo)

                    self.filas[Idx[0]] = nuevaFila

                return self

        if Idx[0] in self.filas.keys():
            for nodo in self.filas[Idx[0]]:
                if nodo[0] == Idx[1]:
                    nodo[1] = v
                    complete = True

            if not complete:
                nodoAnterior = self.filas[Idx[0]].nodoPorCondicion(
                    lambda nodo_temp: nodo_temp.siguiente is None or nodo_temp.siguiente.valor[0] > Idx[1])
                self.filas[Idx[0]].insertarDespuesDeNodo([Idx[1], v], nodoAnterior)

        else:
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].insertarFrente([Idx[1], v])

        return self

    def __mul__(self, k):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        for fila in self.filas.values():
            for nodo in fila:
                nodo[1] *= k
        return self

    def __rmul__(self, k):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__(self, other):
        # Esta funcion implementa la suma de matrices -> A + B

        if self.shape != other.shape:
            raise ValueError("Las matrices son de distinto tamaño")

        """for nro_fila, fila in self.filas.items():
            columnasCompartidas: List[int] = []
            if nro_fila in other.filas.keys():
                for nodo in fila:
                    try:
                        nodoDeOther = fila.nodoPorCondicion(lambda n: n[0] == nodo[0])
                        columnasCompartidas.append(nodo[0])
                    except ValueError:
                        nodoDeOther = 0
                    finally:
                        nodo[1] += nodoDeOther[1]
                
                for nodo in other.filas[nro_fila]:
                    if nodo[0] not in columnasCompartidas:
                        #INCOMPLETO
                """

        """for nro_fila in self.filas.keys(): #TERMINAR
            if nro_fila in other.filas.keys():
                for nodo in self.filas[nro_fila]:"""

        res = MatrizRala(self.shape[0], self.shape[1])

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i, j] = self[i, j] + other[i, j]

        return res

    def __sub__(self, other):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        return self + (-1) * other

    def __matmul__(self, other):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las matrices no tienen tamaños validos para el producto matricial")

        res: MatrizRala = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                posCalculating = 0
                for k in range(self.shape[1]):
                    posCalculating += (self[i, k] * other[k, j])
                res[i, j] = posCalculating
        return res

    def __repr__(self):
        res = 'MatrizRala([ \n'
        for i in range(self.shape[0]):
            res += '    [ '
            for j in range(self.shape[1]):
                res += str(self[i, j]) + ' '

            res += ']\n'

        res += '])'

        return res


def GaussJordan(A, b):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    #Chequear que el tamaño de b sea correcto. Chequear al inicio si b tiene alguna posicion que no es 0 y en A esa fila es todo 0's

    cantPivotes = min(A.shape[0], A.shape[1])
    matriz_temp_gj = A
    for pos_pivotes in range(cantPivotes):
        pivote = A[pos_pivotes, pos_pivotes]
        print("pivote", pivote)
        if pivote != 0:
            if pivote != 1:
                nodo = matriz_temp_gj.filas[pos_pivotes].raiz
                while nodo is not None:
                    print("pos", nodo.valor)
                    matriz_temp_gj[pos_pivotes, nodo.valor[0]] /= pivote
                    nodo = nodo.siguiente

                b[pos_pivotes, 0] /= pivote

            print("primera", repr(matriz_temp_gj))
            filas_a_restar = list(matriz_temp_gj.filas.keys()).copy()
            filas_a_restar.remove(pos_pivotes)
            for fila in filas_a_restar:
                multiplicador: float = matriz_temp_gj[fila, pos_pivotes]
                if A[fila, pos_pivotes] != 0:
                    nodo = A.filas[pos_pivotes].raiz
                    while nodo is not None:
                        matriz_temp_gj[fila, nodo.valor[0]] = matriz_temp_gj[fila, nodo.valor[0]] - multiplicador*matriz_temp_gj[pos_pivotes, nodo.valor[0]]
                        nodo = nodo.siguiente

                    b[fila, 0] = b[fila, 0] - b[pos_pivotes, 0]*multiplicador

    res = []
    print(repr(matriz_temp_gj), repr(b))
    sol_unica = True
    pos_error = None
    for pos_pivotes in range(cantPivotes):
        if matriz_temp_gj[pos_pivotes, pos_pivotes] == 0:
            sol_unica = False
            pos_error = pos_pivotes

    if not sol_unica:
        if b[pos_error, 0] != 0:
            raise ArithmeticError("El sistema no tiene solucion")
        else:
            raise ArithmeticError("El sistema tiene infinitas soluciones")

    for num in range(b.shape[0]):
        res.append(b[num, 0])

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
    return res

A = MatrizRala(3, 3)
A[0, 0] = 1
A[0, 2] = -2
A[1, 1] = 2
A[0, 1] = 3
A[2, 1] = 2
A[2, 2] = 7

B = MatrizRala(3, 3)

B[0, 0] = 1
B[0, 2] = 2
B[2, 2] = 4
B[2, 1] = 2
B[0, 1] = 1

A_mas_B = A + B
print(repr(A))
print(repr(B))
print("A+B: ", repr(A_mas_B))
A * 4
print(repr(A))
A[0, 0] = 0
print("cero", repr(A))
print(repr(B))
print(A @ B)

C = MatrizRala(2, 3)
D = MatrizRala(3, 3)

C[0, 0] = 1
C[0, 2] = 3
C[1, 2] = 4
C[1, 2] = 2

D[2, 0] = 3
D[1, 1] = 2
D[2, 1] = 4

print("C: ", repr(C), " D: ", repr(D))

E = C @ D
print("E: ", repr(E))

F = MatrizRala(3,3)
F[0, 0] = 2
F[1, 0] = -4
F[0, 1] = 8
F[1, 1] = 6
F[0, 2] = 4
F[1, 2] = -8
F[2, 0] = -1
F[2, 1] = -1
F[2, 2] = -2

print(f"F: {repr(F)}")
b = MatrizRala(3, 1)
b[0, 0] = 1
b[1, 0] = 0
b[2, 0] = -2
print(f"b: {repr(b)}")
print(f"Gauss-Jordan de F con b: {GaussJordan(F, b)}")

#Ejercicio 3

matriz_papers = MatrizRala(11, 11)
