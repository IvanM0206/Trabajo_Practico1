from typing import List, Dict, Tuple
from matricesRalas import MatrizRala
from Gauss_Jordan import GaussJordan
import math, time, csv
import numpy as np
from funciones_utiles import norma

# EJERCICIO 4

print("----------EJERCICIO 4-------------")

N = 0 # Cantidad total de papers
citas_recibidas = {}
citados = []
d = 0.85
epsilon = 0.000001
# citas es un dict que para todo paper me dice quienes lo citaron (lista de ids)
# y me dice a cuantos cita en la posición 0

with open('papers/papers.csv', newline='', encoding="utf-8") as csvfile:
    quotations = csv.DictReader(csvfile)
    for row in quotations:
        N += 1

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
    unos[i,0] = 1

# ---------------------------------------


print("Empieza la accion")

vector_prueba = MatrizRala(5, 1)

vector_prueba[0, 0] = 1
vector_prueba[1, 0] = 1
vector_prueba[2, 0] = 1
vector_prueba[3, 0] = 1
vector_prueba[4, 0] = 1

#print(norma(vector_prueba))

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

    p_next = unos * ((1-d)/N) + (d*W@D@p_t)
    
    fin = time.time()

    print(f"Finalizo la iteracion, tardo: {fin-inicio}s")

print("Termino el algoritmo")

# ---------------------------------------

# SE HALLA EL TOP 10 DE PAPERS SEGUN LA CANTIDAD DE CITADOS


diezPopulares: Dict[int, int] = dict() # La clave es el paper y el valor es la cantidad de citas que recibe
for paper, lista_citas in citas_recibidas.items():
    if len(diezPopulares) < 10:
        diezPopulares[paper] = len(lista_citas)
    else:
        citasMenosPopular: int = 1e10
        paperMenosPopular: int = None
        for clave, valor in diezPopulares.items():
            if valor < citasMenosPopular:
                paperMenosPopular = clave
                citasMenosPopular = valor

        if len(lista_citas) > citasMenosPopular:
            diezPopulares.pop(paperMenosPopular)
            diezPopulares[paper] = len(lista_citas)


# ---------------------------------------

# SE HALLA EL TOP 10 DE PAPERS SEGUN EL ALGORITMO

diezImpacto: Dict[int, float] = dict()
for nro_paper, fila in p_next.filas.items():
    valorFinal: float = fila.raiz.valor[1]
    if len(diezImpacto) < 10:
        diezImpacto[nro_paper] = valorFinal
    else:
        menosImpacto: int = 1e10
        paperMenosImpacto: int = None
        for clave, valor in diezImpacto.items():
            if valor < menosImpacto:
                paperMenosImpacto = clave
                menosImpacto = valor

        if valorFinal > menosImpacto:
            diezImpacto.pop(paperMenosImpacto)
            diezImpacto[nro_paper] = valorFinal

# ---------------------------------------



print("Busco los nombres de los dos top 10 encontrados...")

nombresAlgoritmo: List[Tuple[str, int, float]] = []
nombresCitasRecibidas: List[Tuple[str, int, int]] = []
with open('papers/papers.csv', newline='', encoding="utf-8") as csvfile:
    quotations = csv.DictReader(csvfile)
    for row in quotations:
        if int(row["id"]) in diezPopulares.keys():
            nombresCitasRecibidas.append((row["titulo"], int(row["id"]), diezPopulares[int(row["id"])]))
        if int(row["id"]) in diezImpacto.keys():
            nombresAlgoritmo.append((row["titulo"], int(row["id"]), diezImpacto[int(row["id"])]))

nombresAlgoritmo.sort(key=lambda x : x[2], reverse=True)

print("Papers con mayor impacto")
for nombre in nombresAlgoritmo: 
    print(f"Paper: {nombre[0]}, id: {nombre[1]}, proba:{nombre[2]}")

nombresCitasRecibidas.sort(key=lambda x : x[2], reverse=True)

print("\n")
print("Papers con más citas")
for nombre in nombresCitasRecibidas: 
    print(f"Paper: {nombre[0]}, id: {nombre[1]}, citas recibidas:{nombre[2]}")