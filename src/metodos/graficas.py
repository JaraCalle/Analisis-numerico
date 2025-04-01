import numpy as np
import matplotlib.pyplot as plt
import math

import numpy as np
import matplotlib.pyplot as plt
import math

def graficar(fx, titulo_grafica):
    x_values = np.linspace(-10, 10, 1000)
    y_values = [eval(fx, {'x': x, 'math': math}) for x in x_values]
    
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    
    # Cambiar el color de los ejes en x=0 y y=0 (puedes poner cualquier color)
    ax.spines['bottom'].set_color('black')  # Color del eje x
    ax.spines['left'].set_color('black')    # Color del eje y
    
    # Si deseas que el centro de los ejes (x=0 y y=0) sea más visible, haz estos cambios
    ax.axhline(0, color='black', linewidth=0.5)  # Línea horizontal en y=0
    ax.axvline(0, color='black', linewidth=0.5)  # Línea vertical en x=0
    
    # Opcional: Cambiar el grosor de las líneas de las cuadrículas
    ax.grid(True, linewidth=1.5)
    
    # Configurar las etiquetas y el título
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(titulo_grafica)
    ax.grid(True)
    ax.legend()
    ax.set_ylim([-100, 100])
    plt.show()