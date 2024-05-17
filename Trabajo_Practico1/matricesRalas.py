# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan
from typing import Dict, List

# Matrices papers


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
            anteUltimoNodo = self.nodoPorCondicion(
                lambda n: n.siguiente.siguiente is None
            )
            anteUltimoNodo.siguiente = None

        self.longitud -= 1

        return self

    def nodoPorCondicion(self, funcionCondicion):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError("No hay nodos en la lista")

        nodoActual = self.raiz
        while not funcionCondicion(nodoActual):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError("Ningun nodo en la lista satisface la condicion")

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
        res = "ListaEnlazada([ "

        for valor in self:
            res += str(valor) + " "

        res += "])"

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
                    nodoAEliminar = self.filas[Idx[0]].nodoPorCondicion(
                        lambda nodo_temp: nodo_temp.valor[0] == Idx[1]
                    )
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
                    lambda nodo_temp: nodo_temp.siguiente is None
                    or nodo_temp.siguiente.valor[0] > Idx[1]
                )
                self.filas[Idx[0]].insertarDespuesDeNodo([Idx[1], v], nodoAnterior)

        else:
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].insertarFrente([Idx[1], v])

        return self

    def __mul__(self, k):
        # Esta funcion implementa el producto matriz-escalar -> A * k

        """if k == 0:

        claves: List[int] = list(self.filas.keys()).copy()
        i = 0
        while len(self.filas) > 0:
            while len(self.filas[i]) > 0:
                self.filas[i].pop()

            self.filas.pop(claves[i])
            i += 1
        """

        if k == 0:
            return MatrizRala(self.shape[0], self.shape[1])

        else:

            for fila in self.filas.values():
                for nodo in fila:
                    nodo[1] *= k

        return self

    def __eq__(self, other):
        if self.shape != other.shape:
            raise ValueError("Las matrices son de distinto tamaño")

        for fila in range(self.shape[0]):
            for columna in range(self.shape[1]):
                if self[fila, columna] != other[fila, columna]:
                    return False
        return True

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

        # for i in range(self.shape[0]):
        #    for j in range(self.shape[1]):
        #        res[i, j] = self[i, j] + other[i, j]

        # OTRA FORMA: MAS EFICIENTE?
        interseccion_filas: List[int] = list(
            set(self.filas.keys()) & set(other.filas.keys())
        )
        for nro_fila in interseccion_filas:
            nodo_self = self.filas[nro_fila].raiz
            nodo_other = other.filas[nro_fila].raiz

            while nodo_self is not None and nodo_other is not None:
                if nodo_self.valor[0] < nodo_other.valor[0]:
                    res[nro_fila, nodo_self.valor[0]] = nodo_self.valor[1]
                    nodo_self = nodo_self.siguiente

                elif nodo_self.valor[0] > nodo_other.valor[0]:
                    res[nro_fila, nodo_other.valor[0]] = nodo_other.valor[1]
                    nodo_other = nodo_other.siguiente

                else:
                    res[nro_fila, nodo_self.valor[0]] = (
                        nodo_self.valor[1] + nodo_other.valor[1]
                    )
                    nodo_self = nodo_self.siguiente
                    nodo_other = nodo_other.siguiente

            if nodo_self is None:
                while nodo_other is not None:
                    res[nro_fila, nodo_other.valor[0]] = nodo_other.valor[1]
                    nodo_other = nodo_other.siguiente

            elif nodo_other is None:
                while nodo_self is not None:
                    res[nro_fila, nodo_self.valor[0]] = nodo_self.valor[1]
                    nodo_self = nodo_self.siguiente

        solo_en_self = list(set(self.filas.keys()) - set(other.filas.keys()))
        for nro_fila in solo_en_self:
            for nodo in self.filas[nro_fila]:
                res[nro_fila, nodo[0]] = nodo[1]

        solo_en_other = list(set(other.filas.keys()) - set(self.filas.keys()))
        for nro_fila in solo_en_other:
            for nodo in other.filas[nro_fila]:
                res[nro_fila, nodo[0]] = nodo[1]

        return res

    def __sub__(self, other):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        return self + (-1) * other

    def __matmul__(self, other):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise ValueError(
                "Las matrices no tienen tamaños válidos para el producto matricial"
            )

        res: MatrizRala = MatrizRala(self.shape[0], other.shape[1])
        """for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                posCalculating = 0
                for k in range(self.shape[1]):
                    posCalculating += self[i, k] * other[k, j]
                res[i, j] = posCalculating"""
        
        """for nro_fila, fila in self.filas.items():
            for columna_other in range(other.shape[1]):
                nodo_self = fila.raiz
                valor = 0
                while nodo_self is not None:
                    valor += nodo_self.valor[1]*other[nodo_self.valor[0], columna_other]
                    try:
                        nodo_columna = other.filas[nodo_self.valor[0]].nodoPorCondicion(lambda nodo: nodo.valor[0] == columna_other)
                        valor += nodo_columna.valor[1]*nodo_self.valor[1]
                    
                    except:
                        valor += 0

                    finally:
                        nodo_self = nodo_self.siguiente
                    nodo_self = nodo_self.siguiente

                res[nro_fila, columna_other] = valor"""

        for filaOrigen in self.filas.keys():
            nodoSelf = self.filas[filaOrigen].raiz

            while nodoSelf is not None:
                if nodoSelf.valor[0] in other.filas.keys():
                    nodoOther = other.filas[nodoSelf.valor[0]].raiz
                    while nodoOther is not None:
                        res[filaOrigen, nodoOther.valor[0]] += (
                            nodoSelf.valor[1] * nodoOther.valor[1]
                        )
                        nodoOther = nodoOther.siguiente

                nodoSelf = nodoSelf.siguiente
                
        return res

    def __repr__(self):
        res = "MatrizRala([ \n"
        for i in range(self.shape[0]):
            res += "    [ "
            for j in range(self.shape[1]):
                res += str(self[i, j]) + " "

            res += "]\n"

        res += "])"

        return res
