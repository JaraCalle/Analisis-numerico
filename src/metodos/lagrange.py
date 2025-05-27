import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion

def lagrange(x, y, x_real=None, y_real=None):
  n = len(x) # Número de puntos

  # Matriz para ir guardando cada polinomio
  # Cada fila será un polinomio Li(x)*y_i, del mismo tamaño (n términos como máximo)
  tabla = np.zeros((n, n))

  # Recorremos cada punto (x_i, y_i)
  for i in range(n):
    Li = np.array([1.0]) # Se inicializa el polinomio con un array de numpy
    denominador = 1.0 # Se inicializa el denominador

    # Loop para construir el polinomio
    for j in range(n):
      if j != i:
        paux = np.array([1.0, -x[j]])  # (x - x_j)
        Li = np.convolve(Li, paux) # Multiplicamos acumulativamente Li por (x - x_j)
        denominador *= (x[i] - x[j]) # Acumulamos el denominador: producto de (x_i - x_j)

    tabla[i, n - len(Li):] = y[i] * Li / denominador # Se guarda el polinomio en la tabla

  pol = np.sum(tabla, axis=0) # Sumamos todos los polinomios L_i(x) * y_i para obtener el polinomio interpolante total

  polinomio = imprimir_polinomio(pol, n)

  # Se evalúa el error convencional
  if x_real is not None and y_real is not None:
    error = calcular_error_interpolacion(pol, x_real, y_real)
    
  graph = graficar_interpolacion(x, y, pol, x_real, y_real, "Lagrange")

  return polinomio, error, graph