from django.shortcuts import render
from django.contrib import messages
import pandas as pd
import random
from .graficas import graficar
from .biseccion import biseccion_CS, biseccion_DC
from .regla_falsa import regla_falsa_CS, regla_falsa_DC
from .punto_fijo import punto_fijo_CS, punto_fijo_DC
from .newton import newton_CS, newton_DC
from .secante import secante_CS, secante_DC
from .raices_multiples import newton_m2_CS, newton_m2_DC
from .jacobi_seidel import MatJacobiSeid_DC, MatJacobiSeid_CS1, MatJacobiSeid_CS2
from .sor import SOR_DC, SOR_CS1, SOR_CS2
from .vandermonde import vandermonde
from .newton_int import newtonint
from .lagrange import lagrange
from .spline import spline

def inicio(request):
    df_enl = None
    grafico_enl = None
    df_reporte_enl = None
    reporte_enl = None
    df_iterativos = None
    reporte_iterativos = None
    polinomio_int = None
    error_int = None
    grafica_int = None
    reporte_int = None
    grafica_reporte_int = None

    diccionario = {'tabla_enl': df_enl, 'grafico_enl': grafico_enl, 'tabla_reporte_enl': df_reporte_enl, 'reporte_enl': reporte_enl,
                    'tabla_iterativos': df_iterativos, 'reporte_iterativos': reporte_iterativos, 'polinomio_int': polinomio_int,
                    'error_int': error_int, 'grafica_int': grafica_int, 'reporte_int': reporte_int, 'grafica_reporte_int': grafica_reporte_int,
                    'formulario_activo': "enl"}
    

    if request.method == "POST":
        formulario = request.POST.get("formulario")

        if formulario == "enl":
            df_enl, grafico_enl = enl(request)
            diccionario["tabla_enl"] = df_enl
            diccionario["grafico_enl"] = grafico_enl
            diccionario["formulario_activo"] = "enl"
            return render(request, 'inicio.html', diccionario)

        elif formulario == "reporte_enl":
            df_reporte_enl, reporte_enl = crear_reporte_enl(request)
            diccionario["tabla_reporte_enl"] = df_reporte_enl
            diccionario["reporte_enl"] = reporte_enl
            diccionario["formulario_activo"] = "reporte_enl"
            return render(request, 'inicio.html', diccionario)
        
        elif formulario == "iterativos":
            df_iterativos, reporte_iterativos = iterativos(request)
            diccionario["tabla_iterativos"] = df_iterativos
            diccionario["reporte_iterativos"] = reporte_iterativos
            diccionario["formulario_activo"] = "iterativos"
            return render(request, 'inicio.html', diccionario)
        
        elif formulario == "interpolacion":
            polinomio_int, error_int, grafica_int = interpolacion(request)
            diccionario["polinomio_int"] = polinomio_int
            diccionario["error_int"] = error_int
            diccionario["grafica_int"] = grafica_int
            diccionario["formulario_activo"] = "interpolacion"
            return render(request, 'inicio.html', diccionario)
        
        elif formulario == "reporte_interpolacion":
            reporte, grafica_reporte_int = reporte_interpolacion(request)
            diccionario["reporte_int"] = reporte
            diccionario["grafica_reporte_int"] = grafica_reporte_int
            diccionario["formulario_activo"] = "reporte_interpolacion"
    
    return render(request, 'inicio.html', diccionario)

def enl(request):
    metodo = request.POST.get("metodo")
    tipo_error = request.POST.get("tipo_error")  # 'DC' o 'CS'
    tolerancia = request.POST.get("tolerancia")
    fx = request.POST.get("funcion")
    iteraciones = int(request.POST.get("iteraciones"))

    # Nombre dinámico de la función, ej: biseccion_DC
    nombre_funcion = f"{metodo.lower().replace(' ', '_')}_{tipo_error}"

    # Obtener la función desde el módulo
    funcion_metodo = globals().get(nombre_funcion)

    if not funcion_metodo:
        messages.error(request, "Método no encontrado.")
        return None, None

    try:
        if metodo in ["Biseccion", "Regla Falsa"]:
            a = float(request.POST.get("inferior"))
            b = float(request.POST.get("superior"))
            df, grafico = funcion_metodo(a, b, tolerancia, iteraciones, fx, request)

        elif metodo == "Punto Fijo":
            g = request.POST.get("g")
            x0 = float(request.POST.get("punto_inicial"))
            df, grafico = funcion_metodo(x0, g, tolerancia, iteraciones, fx, request)

        elif metodo == "Newton":
            df1 = request.POST.get("derivada")
            x0 = float(request.POST.get("punto_inicial"))
            df, grafico = funcion_metodo(x0, tolerancia, iteraciones, fx, df1, request)

        elif metodo == "Newton M2":
            df1 = request.POST.get("derivada")
            df2 = request.POST.get("segunda_derivada")
            x0 = float(request.POST.get("punto_inicial"))
            df, grafico = funcion_metodo(x0, tolerancia, iteraciones, fx, df1, df2, request)

        elif metodo == "Secante":
            x0 = float(request.POST.get("punto_inicial_1"))
            x1 = float(request.POST.get("punto_inicial_2"))
            df, grafico = funcion_metodo(x0, x1, tolerancia, iteraciones, fx, request)
        
        if df:
            df = df.to_html(classes='table table-striped', index=False)

        if grafico is None:
            grafico = graficar(fx)
        
        return df, grafico

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None

def crear_reporte_enl(request):
    tipo_error = request.POST.get("tipo_error")
    tolerancia = request.POST.get("tolerancia")
    fx = request.POST.get("funcion")
    iteraciones = int(request.POST.get("iteraciones"))

    try:
        a = float(request.POST.get("inferior"))
        b = float(request.POST.get("superior"))
        g = request.POST.get("g")
        x0 = float(request.POST.get("punto_inicial_1"))
        x1 = float(request.POST.get("punto_inicial_2"))
        derivada1 = request.POST.get("derivada")
        derivada2 = request.POST.get("segunda_derivada")

        if tipo_error == 'DC':
            df_bis, grafico = biseccion_DC(a, b, tolerancia, iteraciones, fx, request)
            df_rf, grafico = regla_falsa_DC(a, b, tolerancia, iteraciones, fx, request)
            df_pf, grafico = punto_fijo_DC(x0, g, tolerancia, iteraciones, fx, request)
            df_newton, grafico = newton_DC(x0, tolerancia, iteraciones, fx, derivada1, request)
            df_secante, grafico = secante_DC(x0, x1, tolerancia, iteraciones, fx, request)
            df_rm, grafico = newton_m2_DC(x0, tolerancia, iteraciones, fx, derivada1, derivada2, request)
        
        elif tipo_error == 'CS':
            df_bis, grafico = biseccion_CS(a, b, tolerancia, iteraciones, fx, request)
            df_rf, grafico = regla_falsa_CS(a, b, tolerancia, iteraciones, fx, request)
            df_pf, grafico = punto_fijo_CS(x0, g, tolerancia, iteraciones, fx, request)
            df_newton, grafico = newton_CS(x0, tolerancia, iteraciones, fx, derivada1, request)
            df_secante, grafico = secante_CS(x0, x1, tolerancia, iteraciones, fx, request)
            df_rm, grafico = newton_m2_CS(x0, tolerancia, iteraciones, fx, derivada1, derivada2, request)

        soluciones = [df_bis, df_rf, df_pf, df_newton, df_secante, df_rm]
        tabla, reporte = generar_tabla_final(soluciones, iteraciones)
        return tabla, reporte

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None
    
def generar_tabla_final(soluciones, iteraciones):
    i = 0
    for metodo in soluciones:
        if metodo is None:
            soluciones[i] = pd.DataFrame(data={'iter': [iteraciones], 'X': ['No se halló la solución'], 'f(X)': [None], 'E': [1]})
        i += 1
    

    mejor_metodo = hallar_mejor_metodo(soluciones)

    reporte = crear_html(soluciones, mejor_metodo)

    tabla = mejor_metodo.to_html(classes='table table-striped', index=False)

    return tabla, reporte

def hallar_mejor_metodo(soluciones):
    min_iteraciones = 10e10
    mejor_metodo = []

    for metodo in soluciones:
        if metodo.iloc[-1, 0] == min_iteraciones:
            mejor_metodo.append(metodo)
        if metodo.iloc[-1, 0] < min_iteraciones:
            min_iteraciones = metodo.iloc[-1, 0]
            mejor_metodo = [metodo]
    
    if len(mejor_metodo) > 1:
        min_error = 1
        for metodo in mejor_metodo:
            if metodo.iloc[-1, 3] < min_error:
                metodo_final = metodo
    else:
        metodo_final = mejor_metodo[0]

    return metodo_final

def crear_html(soluciones, mejor_metodo):
    print("dentro de reporte")
    if mejor_metodo is soluciones[0]:
        nombre_metodo = "método de la bisección"
    elif mejor_metodo is soluciones[1]:
        nombre_metodo = "método de la regla falsa"
    elif mejor_metodo is soluciones[2]:
        nombre_metodo = "método de punto fijo"
    elif mejor_metodo is soluciones[3]:
        nombre_metodo = "método de Newton"
    elif mejor_metodo is soluciones[4]:
        nombre_metodo = "método de la secante"
    elif mejor_metodo is soluciones[5]:
        nombre_metodo = "método de raíces múltiples"

    reporte = f"""
        <div>
            <ul>
                <li>
                    Bisección: iteraciones &rarr; {soluciones[0].iloc[-1, 0]} | X solución &rarr; {soluciones[0].iloc[-1, 1]} | error &rarr; {soluciones[0].iloc[-1, 3]}
                </li>
                <li>
                    Regla Falsa: iteraciones &rarr; {soluciones[1].iloc[-1, 0]} | X solución &rarr; {soluciones[1].iloc[-1, 1]} | error &rarr; {soluciones[1].iloc[-1, 3]}
                </li>
                <li>
                    Punto Fijo: iteraciones &rarr; {soluciones[2].iloc[-1, 0]} | X solución &rarr; {soluciones[2].iloc[-1, 1]} | error &rarr; {soluciones[2].iloc[-1, 3]}
                </li>
                <li>
                    Newton: iteraciones &rarr; {soluciones[3].iloc[-1, 0]} | X solución &rarr; {soluciones[3].iloc[-1, 1]} | error &rarr; {soluciones[3].iloc[-1, 3]}
                </li>
                <li>
                    Secante: iteraciones &rarr; {soluciones[4].iloc[-1, 0]} | X solución &rarr; {soluciones[4].iloc[-1, 1]} | error &rarr; {soluciones[4].iloc[-1, 3]}
                </li>
                <li>
                    Raíces Múltiples: iteraciones &rarr; {soluciones[5].iloc[-1, 0]} | X solución &rarr; {soluciones[5].iloc[-1, 1]} | error &rarr; {soluciones[5].iloc[-1, 3]}
                </li>
            </ul>
            <p>El mejor método fue el {nombre_metodo}, el cual tuvo una X solución de {mejor_metodo.iloc[-1, 1]}, requiriendo {mejor_metodo.iloc[-1, 0]} 
            iteraciones y con un error de {mejor_metodo.iloc[-1, 3]}.</p>
        </div>
    """
    return reporte

def iterativos(request):
    metodo = request.POST.get("metodo_iterativo")
    tipo_error = request.POST.get("tipo_error")
    tolerancia = request.POST.get("tolerancia")
    iteraciones = int(request.POST.get("iteraciones"))
    w = request.POST.get("peso_w")
    w1 = random.uniform(0.9, 1.1)
    w2 = random.uniform(0.9, 1.1)
    w3 = random.uniform(0.9, 1.1)
    size = request.POST.get("size_A")
    size = int(size)
    A = llenar_matriz_A(size, request)
    b = llenar_vector_b(size, request)
    x0 = llenar_vector_x0(size, request)

    try:
        if tipo_error == 'DC':
            df_jacobi, ro_jacobi = MatJacobiSeid_DC(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel, ro_seidel = MatJacobiSeid_DC(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2, ro_sor2 = SOR_DC(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3, ro_sor3 = SOR_DC(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1, ro_sor1 = SOR_DC(A, b, x0, tolerancia, iteraciones, w, request)
        
        elif tipo_error == 'CS1':
            df_jacobi, ro_jacobi = MatJacobiSeid_CS1(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel, ro_seidel = MatJacobiSeid_CS1(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2, ro_sor2 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3, ro_sor3 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1, ro_sor1 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w, request)
        
        elif tipo_error == 'CS2':
            df_jacobi, ro_jacobi = MatJacobiSeid_CS2(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel, ro_seidel = MatJacobiSeid_CS2(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2, ro_sor2 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3, ro_sor3 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1, ro_sor1 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w, request)

        if metodo == "jacobi":
            if ro_jacobi < 1:
                solucion = f"""
                <p>El radio espectral del método de Jacobi es <span>{ro_jacobi}</span>. Como el radio espectral es menor a 1, el método
                puede converger (cumple el primer criterio del teorema de convergencia).</p><br>
                """
            else:
                solucion = f"""
                <p>El radio espectral del método de Jacobi es <span>{ro_jacobi}</span>. Como el radio espectral es mayor a 1, el método
                puede que no llegue a converger (no cumple el primer criterio del teorema de convergencia).</p><br>
                """
            solucion += df_jacobi.to_html(classes='table table-striped', index=False)

        elif metodo == "seidel":
            if ro_seidel < 1:
                solucion = f"""
                <p>El radio espectral del método de Gauss-Seidel es <span>{ro_seidel}</span>. Como el radio espectral es menor a 1, el método
                puede converger (cumple el primer criterio del teorema de convergencia).</p><br>
                """
            else:
                solucion = f"""
                <p>El radio espectral del método de Gauss-Seidel es <span>{ro_seidel}</span>. Como el radio espectral es mayor a 1, el método
                puede que no llegue a converger (no cumple el primer criterio del teorema de convergencia).</p><br>
                """
            solucion += df_seidel.to_html(classes='table table-striped', index=False)

        elif metodo == "sor":
            if ro_sor1 < 1:
                solucion = f"""
                <p>El radio espectral del método de SOR es <span>{ro_sor1}</span>. Como el radio espectral es menor a 1, el método
                puede converger (cumple el primer criterio del teorema de convergencia).</p><br>
                """
            else:
                solucion = f"""
                <p>El radio espectral del método de SOR es <span>{ro_sor1}</span>. Como el radio espectral es mayor a 1, el método
                puede que no llegue a converger (no cumple el primer criterio del teorema de convergencia).</p><br>
                """
            solucion += df_sor1.to_html(classes='table table-striped', index=False)

        tabla = comparar_iterativos(df_jacobi, df_seidel, df_sor1, df_sor2, df_sor3, size)

        comparacion = f"""
            {tabla}
            <p>Los pesos usados en SOR fueron {w}, {w2} y {w3}, respectivamente.</p>
            """

        return solucion, comparacion

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None

def llenar_matriz_A(size, request):
    A = [[None for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            aij = request.POST.get(f"a{i+1}{j+1}")
            A[i][j] = float(aij)
    
    return A

def llenar_vector_b(size, request):
    b = [None] * size
    
    for i in range(size):
        bi = request.POST.get(f"b{i+1}")
        b[i] = float(bi)

    return b

def llenar_vector_x0(size, request):
    x0 = [None] * size
        
    for i in range(size):
        xi = request.POST.get(f"x{i+1}")
        x0[i] = float(xi)

    return x0

def comparar_iterativos(df_jacobi, df_seidel, df_sor1, df_sor2, df_sor3, n):
    metodos = {'Jacobi': df_jacobi, 'Gauss-Seidel': df_seidel, 'Sor 1': df_sor1, 'Sor 2': df_sor2, 'Sor 3': df_sor3}

    columnas = ["Método", "Iteraciones"]
    for i in range(n):
        columnas.append(f'X{i+1}')
    columnas.append("Error Final")

    tabla = pd.DataFrame(columns=columnas)
    
    mejor_metodo = None
    menor_iter = float('inf')

    for nombre_metodo, df_metodo in metodos.items():
        ultima_fila = df_metodo.iloc[-1]
        iteraciones = ultima_fila.iloc[0] 

        if iteraciones < menor_iter:
            menor_iter = iteraciones
            mejor_metodo = nombre_metodo
            
        nueva_fila = [nombre_metodo] + ultima_fila.tolist()
        tabla.loc[len(tabla)] = nueva_fila
    
    # Convertir tabla a HTML
    tabla_html = tabla.to_html(classes='table table-striped', index=False)
    
    # Agregar mensaje sobre el mejor método
    tabla_html += f'''
    <div class="alert alert-success mt-3">
        <strong>Mejor método:</strong> {mejor_metodo} con {menor_iter} iteraciones.
    </div>
    '''
    
    return tabla_html

def interpolacion(request):
    valores_x = request.POST.get("valores_x")
    valores_y = request.POST.get("valores_y")
    metodo = request.POST.get("metodo_int")
    x_real = request.POST.get("x_real")
    y_real = request.POST.get("y_real")

    try:
        valores_x = [float(num.strip()) for num in valores_x.split(',') if num.strip() != '']
        valores_y = [float(num.strip()) for num in valores_y.split(',') if num.strip() != '']
    except ValueError:
        messages.error(request, "Por favor ingresar solo números separados por comas en los campos de valores de x y valores de y.")
        return None, None, None
    
    try:
        x_real = float(x_real)
        y_real = float(y_real)
    except:
        messages.error(request, "Por favor ingresar solo números en los campos de valor adicional de x y valor adicional de y.")
        return None, None, None
    
    try:
        if metodo == "Vandermonde":
            polinomio_int, error_int, grafica_int = vandermonde(valores_x, valores_y, x_real, y_real)

        elif metodo == "Newton Interpolante":
            polinomio_int, error_int, grafica_int = newtonint(valores_x, valores_y, x_real, y_real)

        elif metodo == "Lagrange":
            polinomio_int, error_int, grafica_int = lagrange(valores_x, valores_y, x_real, y_real)

        elif metodo == "Spline Lineal":
            polinomio_int, error_int, grafica_int = spline(valores_x, valores_y, 1, x_real, y_real)

        elif metodo == "Spline Cúbico":
            polinomio_int, error_int, grafica_int = spline(valores_x, valores_y, 3, x_real, y_real)
        
        return polinomio_int, error_int, grafica_int

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None, None

def reporte_interpolacion(request):
    valores_x = request.POST.get("valores_x")
    valores_y = request.POST.get("valores_y")
    x_real = request.POST.get("x_real")
    y_real = request.POST.get("y_real")

    try:
        valores_x = [float(num.strip()) for num in valores_x.split(',') if num.strip() != '']
        valores_y = [float(num.strip()) for num in valores_y.split(',') if num.strip() != '']
    except ValueError:
        messages.error(request, "Por favor ingresar solo números separados por comas en los campos de valores de x y valores de y.")
        return None, None, None
    
    try:
        x_real = float(x_real)
        y_real = float(y_real)
    except:
        messages.error(request, "Por favor ingresar solo números en los campos de valor adicional de x y valor adicional de y.")
        return None, None, None

    try:
        polinomio_vander, error_vander, grafica_vander = vandermonde(valores_x, valores_y, x_real, y_real)
        polinomio_newton, error_newton, grafica_newton = newtonint(valores_x, valores_y, x_real, y_real)
        polinomio_lagrange, error_lagrange, grafica_lagrange = lagrange(valores_x, valores_y, x_real, y_real)
        polinomio_spline1, error_spline1, grafica_spline1 = spline(valores_x, valores_y, 1, x_real, y_real)
        polinomio_spline3, error_spline3, grafica_spline3 = spline(valores_x, valores_y, 3, x_real, y_real)

        error_spline1 = 100 if error_spline1 == None else error_spline1
        error_spline3 = 100 if error_spline3 == None else error_spline3
        
        error_minimo = min(error_vander, error_newton, error_lagrange, error_spline1, error_spline3)

        if error_minimo == error_vander:
            mejor_metodo = "Vandermonde"
            error_final = error_vander
            polinomio_final = polinomio_vander
            grafica_final = grafica_vander

        elif error_minimo == error_newton:
            mejor_metodo = "Newton Interpolante"
            error_final = error_newton
            polinomio_final = polinomio_newton
            grafica_final = grafica_newton

        elif error_minimo == error_lagrange:
            mejor_metodo = "Lagrange"
            error_final = error_lagrange
            polinomio_final = polinomio_lagrange
            grafica_final = grafica_lagrange

        elif error_minimo == error_spline1:
            mejor_metodo = "Spline Lineal"
            error_final = error_spline1
            polinomio_final = polinomio_spline1
            grafica_final = grafica_spline1

        elif error_minimo == error_spline3:
            mejor_metodo = "Spline Cúbico"
            error_final = error_spline3
            polinomio_final = polinomio_spline3
            grafica_final = grafica_spline3

        reporte = f"""
        <p>El mejor método es el método de <span>{mejor_metodo}</span>, el cual obtuvo un error de <span>{error_final}.</span></p><br>
        <p>El polinomio solución con este método es:</p>
        <span>{polinomio_final}</span><br>
        <p>Los demás métodos obtuvieron los siguientes errores:</p>
        <ul>
            <li><span>Vandermonde:</span> {error_vander}</li>
            <li><span>Newton Interpolante:</span> {error_newton}</li>
            <li><span>Lagrange:</span> {error_lagrange}</li>
            <li><span>Spline Lineal:</span> {error_spline1 if error_spline1 != 100 else "No definido en el punto"}</li>
            <li><span>Spline Cúbico:</span> {error_spline3 if error_spline3 != 100 else "No definido en el punto"}</li>
        </ul>
        """

        return reporte, grafica_final

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None
