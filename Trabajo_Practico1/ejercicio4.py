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
epsilon = 0.05
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
    unos[i,0]=1

# ---------------------------------------


print("empieza la accion")

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

    p_next = unos * ((1-d)/N) + d*W@D@p_t
    
    fin = time.time()

    print(f"Finalizo la iteracion, tardo: {fin-inicio}s")

print("Termino el algoritmo")

# ---------------------------------------

# SE HALLA EL TOP 10 DE PAPERS SEGUN LA CANTIDAD DE CITADOS

top_diez_papers_dict: Dict[int, int] = dict() # La clave es el paper y el valor es la cantidad de citas que recibe
for paper, lista_citas in citas_recibidas.items():
    if len(top_diez_papers_dict) < 10:
        top_diez_papers_dict[paper] = len(lista_citas)
    else:
        menor_del_top: int = 1e10
        clave_del_menor: int = None
        for clave, valor in top_diez_papers_dict.items():
            if valor < menor_del_top:
                clave_del_menor = clave
                menor_del_top = valor

        if len(lista_citas) > menor_del_top:
            top_diez_papers_dict.pop(clave_del_menor)
            top_diez_papers_dict[paper] = len(lista_citas)


# ---------------------------------------

# SE HALLA EL TOP 10 DE PAPERS SEGUN EL ALGORITMO

suma_probabilidades: float = 0
papers_con_mayor_impacto: Dict[int, int] = dict()
for nro_paper, fila in p_next.filas.items():
    prob: float = fila.raiz.valor[1]
    if len(papers_con_mayor_impacto) < 10:
        papers_con_mayor_impacto[nro_paper] = prob
    else:
        menor_del_top: int = 1e10
        clave_del_menor: int = None
        for clave, valor in papers_con_mayor_impacto.items():
            if valor < menor_del_top:
                clave_del_menor = clave
                menor_del_top = valor

        if prob > menor_del_top:
            papers_con_mayor_impacto.pop(clave_del_menor)
            papers_con_mayor_impacto[paper] = prob

# ---------------------------------------


print("Busco los nombres de los dos top 10 encontrados...")

res_algoritmo: List[Tuple[str, int]] = []
res_citas_recibidas: List[Tuple[str, int, int]] = []
print(papers_con_mayor_impacto, top_diez_papers_dict)
with open('papers/papers.csv', newline='', encoding="utf-8") as csvfile:
    quotations = csv.DictReader(csvfile)
    for row in quotations:
        if int(row["id"]) in papers_con_mayor_impacto.keys():
            res_algoritmo.append((row["titulo"], int(row["id"])))
        if int(row["id"]) in top_diez_papers_dict.keys():
            res_citas_recibidas.append((row["titulo"], int(row["id"]), top_diez_papers_dict[int(row["id"])]))

print(f" \n Los papers con mayor impacto usando el algoritmo son: {res_algoritmo} \n ")
print(f" \n Los papers con mayor impacto viendo la cantidad de citas recibidas: {res_citas_recibidas} \n")