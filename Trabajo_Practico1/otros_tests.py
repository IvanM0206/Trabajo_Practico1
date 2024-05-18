from matricesRalas import MatrizRala


# Para el ejercicio 3
def solicitar_sistema_a_resolver():
    print(
        "Tranquilo/a con certeza recolectamos todos los datos para formar el sistema Ax = b"
    )
    size_of_matrix_row: int = int(input("Cuantas filas queres que tenga tu matriz: "))

    size_of_matrix_column: int = int(
        input("Cuantas columnas queres que tenga tu matriz: ")
    )

    A = MatrizRala(size_of_matrix_row, size_of_matrix_column)
    for nro_fila in range(size_of_matrix_row):
        for nro_columna in range(size_of_matrix_column):
            valor = float(
                input(
                    f"ingresar el valor de la matriz en la fila {nro_fila + 1} y columna {nro_columna + 1}: "
                )
            )
            if valor != 0:
                A[nro_fila, nro_columna] = valor

    print(f"A: {repr(A)}")
    b = MatrizRala(size_of_matrix_row, 1)
    for nro_fila in range(size_of_matrix_row):
        valor = float(
            input(f"ingresar el valor de la solucion en la fila {nro_fila + 1}: ")
        )
        if valor != 0:
            b[nro_fila, 0] = valor

    print(f"b: {repr(b)}")
    print(f"El sistema a resolver es {A}x = {b}")
    return A, b


# Para el ejercicio 4
def solicitar_matriz():
    print("Tranquilo/a con certeza recolectamos todos los datos para formar la matriz")
    size_of_matrix: int = int(
        input(
            "Cuantas filas/columnas queres que tenga tu matriz (va a ser cuadrada asi que solo se necesita un valor): "
        )
    )

    A = MatrizRala(size_of_matrix, size_of_matrix)
    for nro_fila in range(size_of_matrix):
        for nro_columna in range(size_of_matrix):
            valor = int(
                input(
                    f"ingresar el valor de la matriz en la fila {nro_fila + 1} y columna {nro_columna + 1}: "
                )
            )
            if valor != 0:
                A[nro_fila, nro_columna] = valor

    print(f"la matriz es: {repr(A)}")
    return A


# TESTS METODOS MATRIZ RALA

A = MatrizRala(2, 3)
A[0, 0] = 1
A[0, 2] = -2
A[0, 1] = 3
A[1, 1] = 2
A[1, 0] = -4
A[1, 2] = 8


B = MatrizRala(3, 1)

B[0, 0] = 1
B[1, 0] = 2
B[2, 0] = 1

# A_mas_B = A + B
print(repr(A))
print(repr(B))
# print("A+B: ", repr(A_mas_B))
multuplicacion_A = A * 4
print(multuplicacion_A)
# A[0, 0] = 0
# print("cero", repr(A))
# print(repr(B))
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


# ---------------------------------------

# TESTS GAUSS-JORDAN
