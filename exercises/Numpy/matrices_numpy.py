# Elaborar un código en Python que muestre
# una matriz A de orden n cuyos elementos
# sean generados de manera aleatoria.

import numpy as np
import random

exit = False
matrices = []

def gen_mat(m, n):
    A = np.random.randint(0, 100, size=(m, n))
    print("Matriz generada:")
    print(A)
    if len(matrices) < 2:
        matrices.append(A)
    else:
        print("Se sobreescribirá la mátriz más antigua.")
        matrices.pop(0)
        matrices.append(A)

def show_mat():
    print("\nMatrices actuales: ")
    for mat in matrices:
        print(mat)
        print()

while exit == False:
    print("\nSelecciona que quieres hacer:")
    print("\t a) Generar nueva matriz (máx 2)")
    print("\t b) Ver matrices generadas")
    print("\t c) Multiplicar matrices")
    print("\t   d) exit()")
    print()
    opcion = input("Selecciona la letra de su opción: ")

    if opcion == 'a':
        row, col = input("\nEscribe num de filas y cols: ").split()
        gen_mat(int(row), int(col))

    elif opcion == 'b':
        show_mat()

    elif opcion == 'd':
        print("\nAdiós\n")
        exit = True

    else:
        print("Opción no válida.")
