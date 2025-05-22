"""
Spline: Calcula los coeficienetes de los polinomios de interpolación de
grado d (1, 2, 3) para el conjunto de n datos (x,y),
mediante el método spline.
"""
import numpy as np
from .graficas import graficar_spline_general
from .utils_interpolacion import calcular_error_spline, imprimir_polinomios_spline

def spline(x, y, d, x_real=None, y_real=None):
  n = len(x)
  A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
  b = np.zeros((d+1)*(n-1))

  cua = np.array(x)**2
  cub = np.array(x)**3

  c = 0
  h = 0

  if d == 1:
    for i in range(n-1):
      A[h, c] = x[i]
      A[h, c+1] = 1
      b[h] = y[i]
      c += 2
      h += 1

    c = 0
    for i in range(1, n):
      A[h, c] = x[i]
      A[h, c+1] = 1
      b[h] = y[i]
      c += 2
      h += 1

  elif d == 2:
    for i in range(n-1):
      A[h, c] = cua[i]
      A[h, c+1] = x[i]
      A[h, c+2] = 1
      b[h] = y[i]
      c += 3
      h += 1

    c = 0
    for i in range(1, n):
      A[h, c] = cua[i]
      A[h, c+1] = x[i]
      A[h, c+2] = 1
      b[h] = y[i]
      c += 3
      h += 1

    c = 0
    for i in range(1, n-1):
      A[h, c] = 2*x[i]
      A[h, c+1] = 1
      A[h, c+3] = -2*x[i]
      A[h, c+4] = -1
      b[h] = 0
      c += 3
      h += 1

    A[h, 0] = 2
    b[h] = 0

  elif d == 3:
    for i in range(n-1):
      A[h, c] = cub[i]
      A[h, c+1] = cua[i]
      A[h, c+2] = x[i]
      A[h, c+3] = 1
      b[h] = y[i]
      c += 4
      h += 1

    c = 0
    for i in range(1, n):
      A[h, c] = cub[i]
      A[h, c+1] = cua[i]
      A[h, c+2] = x[i]
      A[h, c+3] = 1
      b[h] = y[i]
      c += 4
      h += 1

    c = 0
    for i in range(1, n-1):
      A[h, c] = 3*cua[i]
      A[h, c+1] = 2*x[i]
      A[h, c+2] = 1
      A[h, c+4] = -3*cua[i]
      A[h, c+5] = -2*x[i]
      A[h, c+6] = -1
      b[h] = 0
      c += 4
      h += 1

    c = 0
    for i in range(1, n-1):
      A[h, c] = 6*x[i]
      A[h, c+1] = 2
      A[h, c+4] = -6*x[i]
      A[h, c+5] = -2
      b[h] = 0
      c += 4
      h += 1

    A[h, 0] = 6*x[0]
    A[h, 1] = 2
    b[h] = 0
    h += 1
    A[h, c] = 6*x[-1]
    A[h, c+1] = 2
    b[h] = 0

  val = np.linalg.solve(A, b)
  tabla = val.reshape((n-1, d+1))

  graph = graficar_spline_general(x, y, tabla, d, x_real, y_real)
  polinomios = imprimir_polinomios_spline(x, tabla, d)
  if x_real is not None and y_real is not None:
    error = calcular_error_spline(x, tabla, x_real, y_real)

  return polinomios, error, graph