"""
Spline: Calcula los coeficienetes de los polinomios de interpolación de
grado d (1, 2, 3) para el conjunto de n datos (x,y),
mediante el método spline.
"""
import numpy as np
from .graficas import graficar_spline_general
from .utils_interpolacion import calcular_error_spline, imprimir_polinomios_spline

def spline(x, y, d, x_real=None, y_real=None):
  n = len(x) # Cantidad de puntos
  A = np.zeros(((d+1)*(n-1), (d+1)*(n-1))) # Matriz banda del método de spline
  b = np.zeros((d+1)*(n-1)) # Vector de resultados

  cua = np.array(x)**2 # Eleva todas las x al cuadrado
  cub = np.array(x)**3 # Eleva todas las x al cubo

  c = 0 # Índice para las columnas de la matriz A
  h = 0 # Índice para las filas de la matriz A y el vector b

  if d == 1: # Spline lineal
    # Primera condición: que el polinomio en x_i dé y_i
    for i in range(n-1):
      A[h, c] = x[i] # coeficiente de a_i
      A[h, c+1] = 1 # coeficiente de b_i
      b[h] = y[i] # b_i
      c += 2 # Se avanzan dos columnas
      h += 1 # Se avanza una fila

    c = 0
    # Se repite pero empezando en p2
    for i in range(1, n):
      A[h, c] = x[i]
      A[h, c+1] = 1
      b[h] = y[i]
      c += 2
      h += 1

  elif d == 2: # Spline cuadrático
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

  elif d == 3: # Spline cúbico
    # Primera condición: que el polinomio en x_i dé y_i
    for i in range(n-1):
      A[h, c] = cub[i] # coeficiente de a_i
      A[h, c+1] = cua[i] # coeficiente de b_i
      A[h, c+2] = x[i] # coeficiente de c_i
      A[h, c+3] = 1 # d_i
      b[h] = y[i]
      c += 4 # Se avanzan 4 columnas
      h += 1 # Se avanza una fila

    c = 0
    # Se repite pero empezando en p2
    for i in range(1, n):
      A[h, c] = cub[i]
      A[h, c+1] = cua[i]
      A[h, c+2] = x[i]
      A[h, c+3] = 1
      b[h] = y[i]
      c += 4
      h += 1

    c = 0
    # Condiciones de la primera derivada
    for i in range(1, n-1):
      # Derivada primer polinomio
      A[h, c] = 3*cua[i]
      A[h, c+1] = 2*x[i]
      A[h, c+2] = 1
      # Derivada del segundo polinomio negativa
      A[h, c+4] = -3*cua[i]
      A[h, c+5] = -2*x[i]
      A[h, c+6] = -1
      b[h] = 0 # Se iguala a 0
      c += 4
      h += 1

    c = 0
    # Condiciones de la segunda derivada
    for i in range(1, n-1):
      # Segunda derivada del primer polinomio
      A[h, c] = 6*x[i]
      A[h, c+1] = 2
      # Segunda derivada del segundo polinomio negativa
      A[h, c+4] = -6*x[i]
      A[h, c+5] = -2
      b[h] = 0 # Se iguala a 0
      c += 4
      h += 1

    # Segunda derivada en los extremos = 0
    # Segunda derivada del primer polinomio
    A[h, 0] = 6*x[0]
    A[h, 1] = 2
    b[h] = 0 # Se iguala a 0

    h += 1 # Se avanza a la siguiente fila
    
    # Segunda derivada del último polinomio
    A[h, c] = 6*x[-1]
    A[h, c+1] = 2
    b[h] = 0 # Se iguala a 0

  val = np.linalg.solve(A, b) # Se resuelve el sistema matricial
  tabla = val.reshape((n-1, d+1)) # Se reorganizan los coeficientes en una tabla: una fila por tramo

  graph = graficar_spline_general(x, y, tabla, d, x_real, y_real)
  polinomios = imprimir_polinomios_spline(x, tabla, d)

  # Calcular error
  if x_real is not None and y_real is not None:
    error = calcular_error_spline(x, tabla, x_real, y_real)

  return polinomios, error, graph