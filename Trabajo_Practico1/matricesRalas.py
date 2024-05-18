# Iván Mondrzak y Federico Peitti

from typing import Dict, List


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

    def eliminarNodo(self, nodoAEliminar):
        # Elimina el nodo objetivo
        if nodoAEliminar == self.raiz:
            self.raiz = nodoAEliminar.siguiente

        else:
            nodoAnterior = self.raiz
            while nodoAnterior.siguiente != nodoAEliminar:
                nodoAnterior = nodoAnterior.siguiente

            nodoAnterior.siguiente = nodoAEliminar.siguiente

        self.longitud -= 1
        return self

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
        # Inicialización de la matriz
        self.filas: Dict[int, ListaEnlazada[ListaEnlazada.Nodo]] = {}
        self.shape = (M, N)

    def __getitem__(self, Idx):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]

        # Si la posición no exise en la matriz
        if Idx[0] >= self.shape[0] or Idx[1] >= self.shape[1]:
            raise IndexError("Esa posicion no existe en la matriz")

        res: int = 0
        # Se itera sobre la fila pedida para buscar si existe un elemento en la columnda dada
        # Caso contrario se devuelve 0
        if Idx[0] in self.filas.keys():
            for nodo in self.filas[Idx[0]]:
                if nodo[0] == Idx[1]:
                    res = nodo[1]

        return res

    def __setitem__(self, Idx, v):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v

        # Para valores incompatibles
        if Idx[0] >= self.shape[0] or Idx[1] >= self.shape[1]:
            raise IndexError("Esa posicion no existe en la matriz")

        complete: bool = False

        # Si se inserta 0, eso equivale a eliminar el nodo o no hacer nada
        if v == 0:
            # Si ya es 0 no se realiza ninguna modificación
            if self[Idx[0], Idx[1]] == 0:
                return self

            else:
                # Si la fila objetivo tiene únicamente un elemento distinto de cero, se elimina
                if len(self.filas[Idx[0]]) == 1:
                    self.filas[Idx[0]].pop()
                    self.filas.pop(Idx[0])
                else:
                    # Si la fila tiene más de un elemento, se elimina el nodo objetivo
                    nodoAEliminar = self.filas[Idx[0]].nodoPorCondicion(
                        lambda nodo_temp: nodo_temp.valor[0] == Idx[1]
                    )
                    self.filas[Idx[0]].eliminarNodo(nodoAEliminar)

                return self

        # Si el elemento a insertar es no nulo

        # Se busca la fila
        if Idx[0] in self.filas.keys():
            # Se itera sobre la fila para chequear que el nodo exista
            for nodo in self.filas[Idx[0]]:
                # Si el nodo existe, se modifica su valor
                if nodo[0] == Idx[1]:
                    nodo[1] = v
                    complete = True

            # Si el nodo no existe, se genera y se conecta con la fila
            if not complete:
                nodoAnterior = self.filas[Idx[0]].nodoPorCondicion(
                    lambda nodo_temp: nodo_temp.siguiente is None
                    or nodo_temp.siguiente.valor[0] > Idx[1]
                )
                self.filas[Idx[0]].insertarDespuesDeNodo([Idx[1], v], nodoAnterior)

        # Si no existe la fila indicada, se crea con un nodo único
        else:
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].insertarFrente([Idx[1], v])

        return self

    def __mul__(self, k):
        # Esta funcion implementa el producto matriz-escalar -> A * k

        res = MatrizRala(self.shape[0], self.shape[1])

        # Si se multiplica por cero, se devuelve una matrizRala vacía
        if k == 0:
            return res

        # Se copia cada valor de la matriz origen multiplicado por el escalar k
        else:
            for nro_fila, fila in self.filas.items():
                for nodo in fila:
                    res[nro_fila, nodo[0]] = nodo[1] * k

        return res

    def __eq__(self, other):
        # Comparación entre matrices

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

        # Si las dimensiones no son compatibles
        if self.shape != other.shape:
            raise ValueError("Las matrices son de distinto tamaño")

        res = MatrizRala(self.shape[0], self.shape[1])

        # Filas en común
        interseccion: List[int] = list(set(self.filas.keys()) & set(other.filas.keys()))

        # Se recorre elemento a elemento por fila
        for nro_fila in interseccion:
            nodo_self = self.filas[nro_fila].raiz
            nodo_other = other.filas[nro_fila].raiz

            while nodo_self is not None and nodo_other is not None:
                # Si sólo hay un elemento en [fila,columna] de la primera, sólo se asigna ese valor
                if nodo_self.valor[0] < nodo_other.valor[0]:
                    res[nro_fila, nodo_self.valor[0]] = nodo_self.valor[1]
                    nodo_self = nodo_self.siguiente

                # Si sólo hay un elemento en [fila,columna] de la segunda, sólo se asigna ese valor
                elif nodo_self.valor[0] > nodo_other.valor[0]:
                    res[nro_fila, nodo_other.valor[0]] = nodo_other.valor[1]
                    nodo_other = nodo_other.siguiente

                # Si hay un elmento en las dos matrices en esa posición, se asigna la suma
                else:
                    res[nro_fila, nodo_self.valor[0]] = (
                        nodo_self.valor[1] + nodo_other.valor[1]
                    )
                    nodo_self = nodo_self.siguiente
                    nodo_other = nodo_other.siguiente

            # Al llegar al final de una fila, la otra no necesariamente se terminó de recorrer
            # Se completan esas entradas de ser el caso
            if nodo_self is None:
                while nodo_other is not None:
                    res[nro_fila, nodo_other.valor[0]] = nodo_other.valor[1]
                    nodo_other = nodo_other.siguiente

            elif nodo_other is None:
                while nodo_self is not None:
                    res[nro_fila, nodo_self.valor[0]] = nodo_self.valor[1]
                    nodo_self = nodo_self.siguiente

        # Para las intersecciones nulas (únicamente en una u otra matriz)
        # se asigna la fila que no sea todos 0s
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

        # Se itera sobre las filas de A
        for filaOrigen in self.filas.keys():
            nodoSelf = self.filas[filaOrigen].raiz

            # Para cada A[i,j] no nulo
            while nodoSelf is not None:
                # Se itera sobre la fila j de B
                if nodoSelf.valor[0] in other.filas.keys():
                    # Sea k el índice de columna iterado de B
                    # Se añade a res[i, k] la multiplicación de A[i,j]*B[j,k]
                    nodoOther = other.filas[nodoSelf.valor[0]].raiz
                    while nodoOther is not None:
                        res[filaOrigen, nodoOther.valor[0]] += (
                            nodoSelf.valor[1] * nodoOther.valor[1]
                        )
                        nodoOther = nodoOther.siguiente

                nodoSelf = nodoSelf.siguiente

        # Esto garantiza que al final de las iteraciones cada res[i,k] tiene la sumatoria de A[i,j]*B[j,k] con 0 <= j < #columnas de A ó #filas de B
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
