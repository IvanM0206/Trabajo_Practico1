# Para correr los tests:
#   1- Instalar pytest: ("pip install pytest")
#   2- Correr en la terminal "pytest tests.py"

import pytest
from matricesRalas import MatrizRala, GaussJordan
import numpy as np


class TestIndexacionMatrices:
    def test_indexarCeros(self):
        A = MatrizRala(3, 3)

        assert np.allclose(np.zeros(9), [A[i, j] for i in range(3) for j in range(3)])

    def test_asignarValor(self):
        A = MatrizRala(3, 3)
        A[0, 0] = 1
        assert A[0, 0] == 1

    def test_asignarDejaCeros(self):
        A = MatrizRala(3, 3)
        A[0, 0] = 1

        assert np.allclose(np.zeros(9), [A[i, j] if (i != j and i != 0) else 0 for i in range(3) for j in range(3)])

    def test_asignarEnMismaFila(self):
        A = MatrizRala(3, 3)
        A[0, 1] = 2
        A[0, 0] = 1

        assert A[0, 1] == 2 and A[0, 0] == 1

    def test_reasignar(self):
        A = MatrizRala(3, 3)
        A[1, 0] = 1
        A[1, 0] = 3

        assert A[1, 0] == 3


class TestSumaMatrices:
    def test_distintasDimensiones(self):
        A = MatrizRala(2, 3)
        B = MatrizRala(3, 3)
        with pytest.raises(Exception) as e_info:
            C = A + B

    def test_sumaCorrectamente(self):
        A = MatrizRala(3, 3)
        B = MatrizRala(3, 3)

        A[0, 0] = 1
        A[0, 2] = 3
        A[2, 2] = 4

        B[0, 2] = 3
        B[1, 1] = 2

        C = A + B
        assert C[0, 0] == 1 and C[0, 2] == 6 and C[2, 2] == 4 and C[1, 1] == 2


class TestProductoPorEscalar:
    def test_escalaCorrectamente(self):
        A = MatrizRala(3, 3)
        A[0, 0] = 1
        A[0, 2] = 3
        A[2, 2] = 4

        C = A * 13
        assert C[0, 0] == (1 * 13) and C[0, 2] == (3 * 13) and C[2, 2] == (4 * 13)


class TestProductoMatricial:
    def test_dimensionesEquivocadas(self):
        A = MatrizRala(2, 3)
        B = MatrizRala(4, 3)
        with pytest.raises(Exception) as e_info:
            C = A @ B

    def test_productoAndaBien(self):
        A = MatrizRala(2, 3)
        B = MatrizRala(3, 3)

        A[0, 0] = 1
        A[0, 2] = 3
        A[1, 2] = 4

        B[2, 0] = 3
        B[1, 1] = 2

        C = A @ B

        assert C.shape[0] == 2 and C.shape[1] == 3 and C[0, 0] == 9 and all(
            [C[i, i] == 0 for i in range(2) for j in range(3) if (i != j and i != 0)])

    def test_productoPorIdentidad(self):
        A = MatrizRala(3, 3)
        Id = MatrizRala(3, 3)

        A[0, 0] = 1
        A[0, 2] = 3
        A[1, 2] = 4

        Id[0, 0] = 1
        Id[1, 1] = 1
        Id[2, 2] = 1

        C1 = A @ Id
        C2 = Id @ A
        assert C1[0, 0] == 1 and C1[0, 2] == 3 and C1[1, 2] == 4 and C2[0, 0] == 1 and C2[0, 2] == 3 and C2[
            1, 2] == 4 and C1.shape == C2.shape and C1.shape == A.shape


class TestGaussJordan:
    def test_gauss_jordan_matriz_singular(self):
        A = MatrizRala(2, 2)
        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 0] = 2
        A[1, 1] = 4

        b = MatrizRala(2, 1)
        b[0, 0] = 3
        b[1, 0] = 6

        with pytest.raises(Exception) as e_info:
            GaussJordan(A, b)

    def test_gauss_jordan_pivote_cero(self):
        A = MatrizRala(2, 2)
        A[0, 0] = 0
        A[0, 1] = 2
        A[1, 0] = 0
        A[1, 1] = 3

        b = MatrizRala(2, 1)
        b[0, 0] = 1
        b[1, 0] = 3

        with pytest.raises(Exception) as e_info:
            GaussJordan(A, b)

    def test_gauss_jordan_infinitas_soluciones(self):
        A = MatrizRala(2, 3)
        A[0, 0] = 1
        A[0, 1] = 2
        A[0, 2] = 3
        A[1, 0] = 4
        A[1, 1] = 5
        A[1, 2] = 6

        b = MatrizRala(2, 1)
        b[0, 0] = 7
        b[1, 0] = 8

        with pytest.raises(Exception) as e_info:
            GaussJordan(A, b)

    def test_gauss_jordan_infinitas_soluciones(self):
        A = MatrizRala(3, 3)
        A[0, 1] = 20
        A[1, 2] = 2
        A[2, 0] = 23

        C = MatrizRala(3, 3)
        C[0, 1] = 20
        C[1, 2] = 2
        C[2, 0] = 23

        b = MatrizRala(3, 1)
        b[0, 0] = 1
        b[1, 0] = 1
        b[2, 0] = 1

        d = MatrizRala(3, 1)
        d[0, 0] = 1
        d[1, 0] = 1
        d[2, 0] = 1

        assert (C @ GaussJordan(A, b)) == d

#####

    def test_gauss_jordan_matriz_no_cuadrada(self):
        # Prueba para verificar el manejo de una matriz no cuadrada
        A = MatrizRala(3, 2)
        A[0, 0] = 2
        A[0, 1] = 3
        A[1, 0] = 1
        A[1, 1] = -1
        A[2, 0] = 3
        A[2, 1] = 2

        b = MatrizRala(3, 1)
        b[0, 0] = 6
        b[1, 0] = 1
        b[2, 0] = 5

        solucion = GaussJordan(A, b)
        solucion_bien = MatrizRala(2, 1)
        solucion_bien[0, 0] = 1
        solucion_bien[1, 0] = 2

    def test_gauss_jordan_singular_no_cuadrada(self):
        # Prueba para verificar el manejo de una matriz singular no cuadrada
        A = MatrizRala(3, 2)
        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 0] = 2
        A[1, 1] = 4
        A[2, 0] = 3
        A[2, 1] = 6

        b = MatrizRala(3, 1)
        b[0, 0] = 3
        b[1, 0] = 6
        b[2, 0] = 9

        with pytest.raises(ArithmeticError, match="El sistema no tiene solucion"):
            GaussJordan(A, b)

    def test_gauss_jordan_infinitas_soluciones_no_cuadrada(self):
        # Prueba para verificar el manejo de un sistema con infinitas soluciones en una matriz no cuadrada
        A = MatrizRala(3, 2)
        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 0] = 2
        A[1, 1] = 4
        A[2, 0] = 3
        A[2, 1] = 6

        b = MatrizRala(3, 1)
        b[0, 0] = 3
        b[1, 0] = 6
        b[2, 0] = 9

        with pytest.raises(ArithmeticError, match="El sistema tiene infinitas soluciones"):
            GaussJordan(A, b)