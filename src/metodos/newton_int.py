import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion

def newtonint(x, y, x_real=None, y_real=None):
  n = len(x)
  tabla = np.zeros((n, n+1))

  for i in range(n):
    tabla[i, 0] = x[i]
    tabla[i, 1] = y[i]

  for j in range(2, n + 1):
    for i in range(j-1, n):
      tabla[i, j] = (tabla[i, j-1] - tabla[i-1, j-1]) / (tabla[i, 0] - tabla[i-j+1, 0])

  coef = [tabla[i, i + 1] for i in range(n)]

  pol = np.array([0.0])
  acum = np.array([1.0])

  for i in range(n):
    term = coef[i] * acum
    if len(term) > len(pol):
      pol = np.pad(pol, (len(term) - len(pol), 0))
    elif len(pol) > len(term):
      term = np.pad(term, (len(pol) - len(term), 0))
    pol = pol + term
    if i < n - 1:
      acum = np.convolve(acum, [1, -x[i]])

  polinomio = imprimir_polinomio(pol, n)
  if x_real is not None and y_real is not None:
    error = calcular_error_interpolacion(pol, x_real, y_real)
  graph = graficar_interpolacion(x, y, pol, x_real, y_real, "Newton Interpolante")

  return polinomio, error, graph