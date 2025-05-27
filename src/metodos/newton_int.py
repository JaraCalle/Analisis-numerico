import numpy as np
from .graficas import graficar_interpolacion
from .utils_interpolacion import imprimir_polinomio, calcular_error_interpolacion

def newtonint(x, y, x_real=None, y_real=None):
  n = len(x) # Cantidad de puntos

  # Crear una tabla de ceros de tamaño n x (n+1)
  # Las dos primeras columnas serán x y y, el resto se usará para las diferencias divididas
  tabla = np.zeros((n, n+1))

  for i in range(n):
    tabla[i, 0] = x[i] # Primera columna de la tabla son los valores de x
    tabla[i, 1] = y[i] # Segunnda columna de la tabla son los valores de y

  # Calcular las diferencias divididas y almacenarlas en las columnas siguientes, donde j son las columna e i son las filas
  for j in range(2, n + 1): # Desde la tercera columna (índice 2) hasta la última
    for i in range(j-1, n): # Recorrer desde la fila j-1 hasta n
      tabla[i, j] = (tabla[i, j-1] - tabla[i-1, j-1]) / (tabla[i, 0] - tabla[i-j+1, 0]) # Fórmula para calcular diferencias divididas

  coef = [tabla[i, i + 1] for i in range(n)] # Extraer los coeficientes de la interpolación (diagonal de la tabla de diferencias empezando por el primer valor de y)

  pol = np.array([0.0]) # Inicializar el polinomio interpolante como 0
  acum = np.array([1.0]) # Representa un acumulado de los productos (x - x0)(x - x1)...(x - xn-1) que multiplican cada coeficiente.

  # Construir el polinomio interpolante
  for i in range(n):
    term = coef[i] * acum # Multiplica el coeficiente por el acumulador

    # Alinear tamaños para poder hacer la suma de polinomios (rellena con ceros si es necesario)
    if len(term) > len(pol):
      pol = np.pad(pol, (len(term) - len(pol), 0)) # np.pad es la función que agrega ceros para dejar igualar los tamaños de pol y term
    elif len(pol) > len(term):
      term = np.pad(term, (len(pol) - len(term), 0))
    
    # Se suma term al polinomio total
    pol = pol + term

    # Actualizar el acumulador si no es el último término
    if i < n - 1:
      acum = np.convolve(acum, [1, -x[i]]) # Multiplica polinomios: acum * (x - x[i])

  polinomio = imprimir_polinomio(pol, n)

  # Si se proporciona un punto extra se calcula el error convencional
  if x_real is not None and y_real is not None:
    error = calcular_error_interpolacion(pol, x_real, y_real)
  graph = graficar_interpolacion(x, y, pol, x_real, y_real, "Newton Interpolante")

  return polinomio, error, graph