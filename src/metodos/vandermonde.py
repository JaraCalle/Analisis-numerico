import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion


def vandermonde(x, y, x_real=None, y_real=None):
    x = np.array(x) # Convierte la lista de puntos x en un arreglo de NumPy
    n = len(x) # Número de puntos
    A = [] # Matriz del sistema lineal
    b = np.array(y) # Vector de términos independientes

    # Se construye la matriz de Vandermonde
    for numero in x:
        fila = []
        # Cada fila contiene potencias decrecientes del valor de x
        for i in range(n - 1, -1, -1): # Esto recorre los números del n - 1 hasta 0, en orden descendente, que sería el exponente de cada número que va en la matriz de Vandermonde
            fila.append(numero**i)
        A.append(fila)

    A = np.array(A) # Convierte A a un arreglo NumPy
    a = np.linalg.solve(A, b) # Resuelve el sistema V*a = y (A*a = b) para obtener los coeficientes del polinomio

    pol = imprimir_polinomio(a, n)

    # Si se proporciona un punto extra se calcula el error convencional
    if x_real is not None and y_real is not None:
        error = calcular_error_interpolacion(a, x_real, y_real)
    else:
        error = None

    graph = graficar_interpolacion(x, y, a, x_real, y_real, "Vandermonde")

    return pol, error, graph