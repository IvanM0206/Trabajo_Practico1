from typing import List, Dict, Tuple
from matricesRalas import MatrizRala
from Gauss_Jordan import GaussJordan
import math, time, csv
import numpy as np
from funciones_utiles import norma


#matriz_A, matriz_b = solicitar_sistema_a_resolver()
#print(f"Gauss-Jordan de A con b: {GaussJordan(matriz_A, matriz_b)}")


# ---------------------------------------

# Ejercicio 3

print("--------------EJERCICIO 3 - USANDO G-J ----------------")

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
    for fila in range(matriz_D.shape[0]):
        valor_pos += matriz_W[fila, pos]

    if valor_pos != 0: # Agregue este if. Antes era directo matriz_D[pos, pos] = valor_pos
        matriz_D[pos, pos] = 1/valor_pos
    else:
        matriz_D[pos, pos] = 0

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
#norma_vector_solucion: float = norma(solucion_al_sistema)
#prob_y_paper_con_mayor_prob: int = (-1e10, None)
for nro_paper, fila in solucion_al_sistema.filas.items():
    prob: float = fila.raiz.valor[1]
#    if prob > prob_y_paper_con_mayor_prob[0]:
#        prob_y_paper_con_mayor_prob = (prob, nro_paper)
    suma_probabilidades += prob

suma: float = 0
for nro_paper, fila in solucion_al_sistema.filas.items():
    prob: float = fila.raiz.valor[1]
    suma = suma + prob/suma_probabilidades
    print(f"La probabilidad del paper {nro_paper} es: {prob/suma_probabilidades}")

print(f"La suma de probabilidades da: {suma}")
#print(f"El paper con mayor probabilidad es: {prob_y_paper_con_mayor_prob}")

# ---------------------------------------


print("------------------METODO ITERATIVO----------------")


# SE CONSTRUYE LA MATRIZ W

matriz_W2 = MatrizRala(11,11)

matriz_W2[1, 0] = 1
matriz_W2[6, 0] = 1
matriz_W2[5, 0] = 1
matriz_W2[0, 2] = 1
matriz_W2[0, 3] = 1
matriz_W2[0, 4] = 1
matriz_W2[8, 5] = 1
matriz_W2[5, 6] = 1
matriz_W2[6, 7] = 1
matriz_W2[7, 8] = 1
matriz_W2[6, 8] = 1
matriz_W2[9, 8] = 1
matriz_W2[4, 10] = 1

print(f"W: {matriz_W2}")

# ---------------------------------------

# SE CONSTRUYE LA MATRIZ D

matriz_D = MatrizRala(matriz_W.shape[0], matriz_W.shape[0])

for pos in range(matriz_D.shape[0]):
    valor_pos = 0
    for fila in range(matriz_D.shape[0]):
        valor_pos += matriz_W2[fila, pos]

    if valor_pos != 0: # Agregue este if. Antes era directo matriz_D[pos, pos] = valor_pos
        matriz_D[pos, pos] = 1/valor_pos
    else:
        matriz_D[pos, pos] = 0

print(f"D: {matriz_D}")

# ---------------------------------------

# SE CONSTRUYE b

b2 = MatrizRala(matriz_W2.shape[0], 1)

for nro_fila in range(b2.shape[0]):
    b2[nro_fila, 0] = (1 - d) / (b2.shape[0])

print(f"b2: {b2}")

# ---------------------------------------

# SE CONSTRUYE EL VECTOR DE 1's

unos = MatrizRala(11,1)
for i in range(11):
    unos[i,0] = 1

# ---------------------------------------

# SE CONSTRUYE p_0

p_t = MatrizRala(11,1)
for i in range(11):
    p_t[i,0] = 1/11

# ---------------------------------------

# ELIJO EL EPSILON Y d

epsilon1: float = 0.01
d = 0.85

# ---------------------------------------

# SE CALCULA LA PRIMERA ITERACION, ES DECIR, SE CONSTRUYE p_1

p_next = unos * ((1-d)/11) + d*matriz_W2@matriz_D@p_t

# ---------------------------------------

# SE EJECUTAN EL RESTO DE ITERACIONES DEL ALGORITMO HASTA QUE CONVERGA

i = 0

while norma((p_next - p_t)) > epsilon1:
    i += 1

    print(f"Inicia la iteracion {i}")
    
    inicio = time.time()

    p_t = p_next
    p_next = unos * ((1-d)/11) + d*matriz_W@matriz_D@p_t
    
    fin = time.time()

    if fin-inicio != 0:
        print(f"Finalizo la iteracion {i}, tardo: {fin-inicio}s")
    else:
        print(f"Finalizo la iteracion {i}")


print("termino el metodo iterativo del ejercicio 3")

# ---------------------------------------

print(p_next)

suma_probabilidades2: float = 0
for nro_paper, fila in p_next.filas.items():
    prob: float = fila.raiz.valor[1]
    suma_probabilidades2 += prob

suma: float = 0
for nro_paper, fila in p_next.filas.items():
    prob: float = fila.raiz.valor[1]
    suma = suma + prob/suma_probabilidades2
    print(f"La probabilidad del paper {nro_paper} es: {prob/suma_probabilidades2}")

print(f"La suma de probabilidades da: {suma}")

# ---------------------------------------