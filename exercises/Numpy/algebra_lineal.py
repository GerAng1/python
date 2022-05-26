# La producción de ciertas máquinas
# requiere considerar las siguientes acciones:
# Montaje de las piezas, ajuste de las partes y control de calidad.
# La empresa produce tres tipos de máquinas: A, B y C.
# La siguiente tabla muestra las horas necesarias
# para llevar a cabo cada una de las acciones
# en cada una de las clases de máquina mencionadas:

#           Máquina A       Máquina B       Máquina C    |   Máx Horas
# Montaje       2               4               3        |      510
# Ajuste        1               2               2        |      270
# Control       2               1               1        |      180

# ¿Existe la posibilidad de producción que consuma todas las horas disponibles?

import numpy as np

A = np.array([[1, 4, 3],[1, 2, 2],[2, 1, 1]])
print("Matriz de Coeficientes:")
print(A)
