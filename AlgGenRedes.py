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

def inicializar_poblacion():
    poblacion = []
    for _ in range(TAM_POBLACION):
        asignacion = np.random.dirichlet(np.ones(NUM_USUARIOS)) * BANDA_TOTAL
        poblacion.append(asignacion)
    return poblacion

def seleccion_ruleta(poblacion, aptitudes):
    aptitud_total = sum(aptitudes)
    seleccion = []
    for _ in range(TAM_POBLACION):
        pick = random.uniform(0, aptitud_total)
        current = 0
        for i, individuo in enumerate(poblacion):
            current += aptitudes[i]
            if current > pick:
                seleccion.append(individuo)
                break
    return seleccion

def cruce(padre1, padre2):
    if random.random() < TASA_CRUCE:
        punto_cruce = random.randint(1, NUM_USUARIOS - 1)
        hijo1 = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
        hijo2 = np.concatenate((padre2[:punto_cruce], padre1[punto_cruce:]))
        return hijo1, hijo2
    return padre1, padre2

def mutacion(individuo):
    if random.random() < TASA_MUTACION:
        idx = random.randint(0, NUM_USUARIOS - 1)
        cambio = random.uniform(-0.1, 0.1) * BANDA_TOTAL
        individuo[idx] = max(0, individuo[idx] + cambio)
        individuo *= BANDA_TOTAL / sum(individuo)
    return individuo

def algoritmo_genetico():
    poblacion = inicializar_poblacion()
    
    for gen in range(GENERACIONES):
        aptitudes = [calcular_aptitud(ind) for ind in poblacion]
        poblacion_seleccionada = seleccion_ruleta(poblacion, aptitudes)
        
        nueva_poblacion = []
        for i in range(0, TAM_POBLACION, 2):
            padre1, padre2 = poblacion_seleccionada[i], poblacion_seleccionada[i + 1]
            hijo1, hijo2 = cruce(padre1, padre2)
            nueva_poblacion.extend([mutacion(hijo1), mutacion(hijo2)])
        
        poblacion = nueva_poblacion
        
        mejor_aptitud = max(aptitudes)
        print(f"Generación {gen + 1}: Mejor aptitud = {mejor_aptitud}")

    mejor_individuo = poblacion[np.argmax([calcular_aptitud(ind) for ind in poblacion])]
    print("\nMejor asignación de ancho de banda encontrada:", mejor_individuo)
    print("Aptitud:", calcular_aptitud(mejor_individuo))

algoritmo_genetico()
