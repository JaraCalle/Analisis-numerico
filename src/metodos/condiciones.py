import sympy as sp
import re
from sympy.calculus.util import continuous_domain
from sympy import Interval
import math


# Diccionario de funciones que quieres convertir
math_to_sympy = {
    'math.sin': 'sin',
    'math.cos': 'cos',
    'math.tan': 'tan',
    'math.exp': 'exp',
    'math.log': 'log',
    'math.sqrt': 'sqrt',
    'math.atan': 'atan',
    'math.asin': 'asin',
    'math.acos': 'acos',
    'math.floor': 'floor',
    'math.ceil': 'ceiling',
    'math.fabs': 'Abs',
    'math.pi': 'pi',
    'math.e': 'E'
}

# Función para transformar string usando la librería math a una expresión que sea interpretable por sympy
def convert_math_to_sympy(fx):
    fx = re.sub(r'math\.e\s*\(', 'exp(', fx) # Maraña para que se reconozca bien math.e()
    for math_func, sympy_func in math_to_sympy.items():
        fx = fx.replace(math_func, sympy_func)
    return fx


# Determinar continuidad en el intervalo [a, b]
def verificar_continuidad(fx, a, b):
    fx = convert_math_to_sympy(fx)
    x = sp.symbols('x')
    try:
        fx = sp.sympify(fx)
        print("Expresión sympy:", fx)
    except Exception as e:
        print("Error al convertir a sympy:", e)
        print("No es posible evaluar continuidad del código")
    
    # Retorna True si la fx es continua en el intervalo o False si no lo es
    return continuous_domain(fx, x, Interval(a, b)).is_Interval

# Determinar si f(a) * f(b) < 0
def verificar_existencia_raiz(fx, a, b):
    fa = eval(fx, {'x': a, 'math': math})
    fb = eval(fx, {'x': b,'math': math})
    if fa * fb < 0:
        return True
    else:
        return False