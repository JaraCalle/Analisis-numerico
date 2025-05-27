import numpy as np

def imprimir_polinomio(a, n):
  polinomio = ""
  for i, coef in enumerate(a):
    exp = n - 1 - i # Exponente del término. Es en orden decreciente porque el vector a tiene los coeficientes en orden descendente (desde an-1 hasta a0)
    coef = round(coef, 4) # Redondear a 4 cifras para que no imprima términos muy largos (se puede quitar para que imprima el polinomio exacto)
    if coef == 0:
      continue # Se omiten términos nulos
    signo = " + " if coef > 0 and i > 0 else " " # Determina el signo del coeficiente
    if exp == 0:
      polinomio += f"{signo}{coef}"
    elif exp == 1:
      polinomio += f"{signo}{coef}x"
    else:
      polinomio += f"{signo}{coef}x^{exp}"

  return polinomio

def calcular_error_interpolacion(a, x_real, y_real):
  y_calculado = np.polyval(a, x_real) # Evalúa el polinomio en x_real
  error = abs(y_calculado - y_real) # Error convencional
  return error

def imprimir_polinomios_spline(x, tabla, d):
  polinomios = ""
  for i in range(len(x) - 1):
    coef = tabla[i] # Coeficientes del tramo i
    tramo = f"[{x[i]}, {x[i+1]}]" # Intervalo del tramo
    polinomio = ""

    for j in range(d + 1):
      c = coef[j] # Coeficiente actual
      exp = d - j # Exponente correspondiente (de mayor a menor)

      if abs(c) < 1e-12:
        continue  # omitir términos muy cercanos a 0

      # Determinar el signo
      if c > 0 and j != 0:
        polinomio += " + "
      elif c < 0:
        polinomio += " - " if j == 0 else " - "

      # Manejo del coeficiente
      abs_c = abs(c)
      if not (abs_c == 1 and exp != 0):
        polinomio += f"{abs_c:.4f}"  # Mostrar coeficiente solo si no es 1 y si el exponente es diferente de 0 (redondeado a 4 cifras decimales)

      # Variable y exponente
      if exp > 0:
        polinomio += "x"
        if exp > 1:
          polinomio += f"^{exp}"

    polinomios += f"p{i+1}(x) en {tramo} = {polinomio}<br>"

  return polinomios


def calcular_error_spline(x, tabla, x_real, y_real):
  # Encontrar el tramo en el que se encuentra x_real
  for i in range(len(x) - 1):
    if x[i] <= x_real <= x[i + 1]:
      # Evaluar el polinomio correspondiente en x_real
      coef = tabla[i]  # Obtener coeficientes del tramo correcto
      y_estimada = np.polyval(coef, x_real) # Evaluar el polinomio en x_real
      error = abs(y_estimada - y_real) # Error convencional
      return error
  
  print("El valor de x_real está fuera del dominio de los datos.")
  return None