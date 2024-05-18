from matricesRalas import MatrizRala

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

#A_mas_B = A + B
print(repr(A))
print(repr(B))
#print("A+B: ", repr(A_mas_B))
A * 4
print(repr(A))
#A[0, 0] = 0
#print("cero", repr(A))
#print(repr(B))
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
