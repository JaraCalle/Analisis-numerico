import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion

def lagrange(x, y, x_real=None, y_real=None):
  n = len(x)
  tabla = np.zeros((n, n))

  for i in range(n):
    Li = np.array([1.0])
    denominador = 1.0

    for j in range(n):
      if j != i:
        paux = np.array([1.0, -x[j]])  # (x - x_j)
        Li = np.convolve(Li, paux)
        denominador *= (x[i] - x[j])

    tabla[i, n - len(Li):] = y[i] * Li / denominador

  pol = np.sum(tabla, axis=0)

  polinomio = imprimir_polinomio(pol, n)
  if x_real is not None and y_real is not None:
    error = calcular_error_interpolacion(pol, x_real, y_real)
  graph = graficar_interpolacion(x, y, pol, x_real, y_real, "Lagrange")

  return polinomio, error, graph