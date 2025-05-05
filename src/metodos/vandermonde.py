import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion


def vandermonde(x, y, x_real=None, y_real=None):
    x = np.array(x)
    n = len(x)
    A = []
    b = np.array(y)

    for numero in x:
        fila = []
        for i in range(n - 1, -1, -1):
            fila.append(numero**i)
        A.append(fila)

    A = np.array(A)
    a = np.linalg.solve(A, b)

    pol = imprimir_polinomio(a, n)
    if x_real is not None and y_real is not None:
        error = calcular_error_interpolacion(a, x_real, y_real)
    else:
        error = None

    graph = graficar_interpolacion(x, y, a, x_real, y_real, "Vandermonde")

    return pol, error, graph