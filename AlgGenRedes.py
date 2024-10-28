import random
import numpy as np

NUM_USUARIOS = 10
BANDA_TOTAL = 1000
TAM_POBLACION = 50
GENERACIONES = 100
TASA_CRUCE = 0.8
TASA_MUTACION = 0.05

def calcular_aptitud(asignacion):
    demanda = [random.randint(50, 150) for _ in range(NUM_USUARIOS)]
    satisfaccion = sum(min(a, d) for a, d in zip(asignacion, demanda))
    desviacion = abs(sum(asignacion) - BANDA_TOTAL)
    penalizacion = desviacion * 0.1
    return satisfaccion - penalizacion

