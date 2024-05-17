from typing import List, Dict, Tuple
from matricesRalas import MatrizRala
from Gauss_Jordan import GaussJordan
import math, time, csv
import numpy as np
from funciones_utiles import norma


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


#matriz_A, matriz_b = solicitar_sistema_a_resolver()
#print(f"Gauss-Jordan de A con b: {GaussJordan(matriz_A, matriz_b)}")


# ---------------------------------------

# Ejercicio 3

#SE CONSTRUYE DE LA MATRIZ W

# matriz_W = solicitar_matriz()
matriz_W = MatrizRala(11, 11)

#for pos in range(matriz_W.shape[0]): #Comente este for
#    matriz_W[pos, pos] = 1

matriz_W[1, 0] = 1
matriz_W[6, 0] = 1
matriz_W[5, 0] = 1
matriz_W[0, 2] = 1
matriz_W[0, 3] = 1
matriz_W[0, 4] = 1
matriz_W[8, 5] = 1
matriz_W[5, 6] = 1
matriz_W[6, 7] = 1
matriz_W[7, 8] = 1
matriz_W[6, 8] = 1
matriz_W[9, 8] = 1
matriz_W[4, 10] = 1

print(f"W: {matriz_W}")

# ---------------------------------------


# SE DETERMINA DEL VALOR DE d
#d = float(input("Valor de probabilidad elegido: "))
d = 0.85
print(f"d: {d}")

# ---------------------------------------


# SE CONSTRUYE DE LA MATRIZ D

matriz_D = MatrizRala(matriz_W.shape[0], matriz_W.shape[0])

for pos in range(matriz_D.shape[0]):
    valor_pos = 0
    for fila in range(matriz_W.shape[0]):
        valor_pos += matriz_W[fila, pos]

    if valor_pos != 0: # Agregue este if. Antes era directo matriz_D[pos, pos] = valor_pos
        matriz_D[pos, pos] = 1/valor_pos
    else:
        matriz_D[pos, pos] = 11

print(f"D: {matriz_D}")

# ---------------------------------------


# SE CONSTRUYE DEL VECTOR b

b = MatrizRala(matriz_W.shape[0], 1)

for nro_fila in range(b.shape[0]):
    b[nro_fila, 0] = (1 - d) / (b.shape[0])

print(f"b: {b}")

# ---------------------------------------

# SE CONSTRUYE DE LA MATRIZ IDENTIDAD

matriz_identidad = MatrizRala(matriz_W.shape[0], matriz_W.shape[1])
for nro_fila in range(matriz_identidad.shape[0]):
    matriz_identidad[nro_fila, nro_fila] = 1

print(f"Identidad: {matriz_identidad}")

# ---------------------------------------

# SE CONSTRUYE DE A = I - d * W @ D

matriz_A = matriz_identidad - d * matriz_W @ matriz_D

print(matriz_A)

# ---------------------------------------

# SE OBTIENE EL VECTOR SOLUCION x DEL SISTEMA Ax=b CON EL A Y b CONSTRUIDOS ANTES

solucion_al_sistema: MatrizRala = GaussJordan(matriz_A, b)
print(f"Gauss-Jordan de 1 - d*W*D con (1-d)/11: {solucion_al_sistema}")

# ---------------------------------------

suma_probabilidades: float = 0 # Agregue todo esto, igual no cambia el resultado
norma_vector_solucion: float = norma(solucion_al_sistema)
prob_y_paper_con_mayor_prob: int = (-1e10, None)
for nro_paper, fila in solucion_al_sistema.filas.items():
    prob: float = fila.raiz.valor[1]
    if prob > prob_y_paper_con_mayor_prob[0]:
        prob_y_paper_con_mayor_prob = (prob, nro_paper)
    suma_probabilidades += prob

suma: float = 0
for nro_paper, fila in solucion_al_sistema.filas.items():
    prob: float = fila.raiz.valor[1]
    suma = suma + prob/suma_probabilidades
    print(f"La probabilidad del paper {nro_paper} es: {prob/suma_probabilidades}")

print(f"suma: {suma}")
print(f"La suma de probabilidades da: {suma_probabilidades}")
print(f"El paper con mayor probabilidad es: {prob_y_paper_con_mayor_prob}")

# ---------------------------------------

# EJERCICIO 4

N = 629814 # Cantidad total de papers
citas_recibidas = {}
citados = []
d = 0.85
epsilon = 0.05
# citas es un dict que para todo paper me dice quienes lo citaron (lista de ids)
# y me dice a cuantos cita en la posición 0

# SE LLENA citas_recibidas

with open('papers/citas.csv', newline='') as csvfile:
    quotations = csv.DictReader(csvfile)
    for row in quotations:
        #N += 1
        
        #N = max(N, int(row["to"]), int(row["from"]))

        if int(row["to"]) not in citas_recibidas.keys():
            citas_recibidas[int(row["to"])] = [int(row["from"])]
        else:
            citas_recibidas[int(row["to"])].append(int(row["from"])) 

    for i in range(N):
        citados.append(0)

# ---------------------------------------

# SE LLENA citados

with open('papers/citas.csv', newline='') as csvfile:
    quotations = csv.DictReader(csvfile)
    for row in quotations:
        citados[int(row["from"])] += 1

# ---------------------------------------

print("Se lleno citados y citas_recibidas")
print(f"El total de papers es: {N}")

# ---------------------------------------


# SE CONSTRUYE LA MATRIZ W

W = MatrizRala(N,N)
for i in citas_recibidas.keys():
  for j in citas_recibidas[i]:
    W[i, j] = 1

# ---------------------------------------

# SE CONSTRUYE LA MATRIZ D

D = MatrizRala(N,N)
for i in range(N):
  if (citados[i] != 0):
    D[i,i] = 1/citados[i]

# ---------------------------------------

# SE CONSTRUYE EL VECTOR DE 1's

unos = MatrizRala(N,1)
for i in range(N):
    unos[i,0]=1

# ---------------------------------------


print("empieza la accion")

vector_prueba = MatrizRala(5, 1)

vector_prueba[0, 0] = 1
vector_prueba[1, 0] = 1
vector_prueba[2, 0] = 1
vector_prueba[3, 0] = 1
vector_prueba[4, 0] = 1

print(norma(vector_prueba))

# ---------------------------------------

# SE ARMA EL VECTOR INICIAL, ES DECIR p_0

p_t = MatrizRala(N,1)
for i in range(N):
    p_t[i,0] = 1/N

#print(p_t[0,0])

# ---------------------------------------

# PRIMERA EJECUCION DEL ALGORITMO

print("Inicia la primera iteracion del algoritmo")

start = time.time()
p_next = unos * ((1-d)/N) + d*W@D@p_t
end = time.time()

#print(p_next[0,0])
print(f"La primera iteracion tardo: {end-start} s")

# ---------------------------------------


print(norma((p_next - p_t)))

# ---------------------------------------

# SE EJECUTAN EL RESTO DE ITERACIONES DEL ALGORITMO HASTA QUE CONVERGA

while norma((p_next - p_t)) > epsilon:

    print("Inicia la iteracion")
    
    inicio = time.time()

    p_t = p_next

    p_next = unos * ((1-d)/N) + d*W@D@p_t
    
    fin = time.time()

    print(f"Finalizo la iteracion, tardo: {fin-inicio}s")

print("Termino el algoritmo")

# ---------------------------------------


suma_probabilidades: float = 0
norma_p_next: float = norma(p_next)
prob_y_paper_con_mayor_prob: int = (-1e10, None)
for nro_paper, fila in p_next.filas.items():
    prob: float = fila.raiz.valor[1]
    if prob > prob_y_paper_con_mayor_prob[0]:
        prob_y_paper_con_mayor_prob = (prob, nro_paper)
    suma_probabilidades += prob/norma_p_next

print(f"La suma de probabilidades da: {suma_probabilidades}")
print(f"El paper con mayor probabilidad es: {prob_y_paper_con_mayor_prob}")
