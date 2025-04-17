from django.shortcuts import render
from django.contrib import messages
import pandas as pd
import random
from .biseccion import biseccion_CS, biseccion_DC
from .regla_falsa import regla_falsa_CS, regla_falsa_DC
from .punto_fijo import punto_fijo_CS, punto_fijo_DC
from .newton import newton_CS, newton_DC
from .secante import secante_CS, secante_DC
from .raices_multiples import newton_m2_CS, newton_m2_DC
from .jacobi_seidel import MatJacobiSeid_DC, MatJacobiSeid_CS1, MatJacobiSeid_CS2
from .sor import SOR_DC, SOR_CS1, SOR_CS2

def inicio(request):
    df_enl = None
    grafico_enl = None
    reporte = None
    df_reporte_enl = None
    reporte_enl = None
    df_iterativos = None
    reporte_iterativos = None
    diccionario = {'tabla_enl': df_enl, 'grafico_enl': grafico_enl, 'tabla_reporte_enl': df_reporte_enl, 'reporte_enl': reporte_enl,
                    'tabla_iterativos': df_iterativos, 'reporte_iterativos': reporte_iterativos, 'formulario_activo': "enl"}
    

    if request.method == "POST":
        formulario = request.POST.get("formulario")

        if formulario == "enl":
            df_enl, grafico_enl = enl(request)
            diccionario = {'tabla_enl': df_enl, 'grafico_enl': grafico_enl, 'tabla_reporte_enl': df_reporte_enl, 'reporte_enl': reporte_enl,
                           'tabla_iterativos': df_iterativos, 'reporte_iterativos': reporte_iterativos, 'formulario_activo': formulario}
            return render(request, 'inicio.html', diccionario)

        elif formulario == "reporte_enl":
            df_reporte_enl, reporte_enl = crear_reporte_enl(request)
            diccionario = {'tabla_enl': df_enl, 'grafico_enl': grafico_enl, 'tabla_reporte_enl': df_reporte_enl, 'reporte_enl': reporte_enl,
                           'tabla_iterativos': df_iterativos, 'reporte_iterativos': reporte_iterativos, 'formulario_activo': formulario}
            return render(request, 'inicio.html', diccionario)
        
        elif formulario == "iterativos":
            df_iterativos, reporte_iterativos = iterativos(request)
            diccionario = {'tabla_enl': df_enl, 'grafico_enl': grafico_enl, 'tabla_reporte_enl': df_reporte_enl, 'reporte_enl': reporte_enl,
                           'tabla_iterativos': df_iterativos, 'reporte_iterativos': reporte_iterativos, 'formulario_activo': formulario}
            return render(request, 'inicio.html', diccionario)
    
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
        
        df = df.to_html(classes='table table-striped', index=False)
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
            df_jacobi = MatJacobiSeid_DC(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel = MatJacobiSeid_DC(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2 = SOR_DC(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3 = SOR_DC(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1 = SOR_DC(A, b, x0, tolerancia, iteraciones, w, request)
        
        elif tipo_error == 'CS1':
            df_jacobi = MatJacobiSeid_CS1(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel = MatJacobiSeid_CS1(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1 = SOR_CS1(A, b, x0, tolerancia, iteraciones, w, request)
        
        elif tipo_error == 'CS2':
            df_jacobi = MatJacobiSeid_CS2(A, b, x0, tolerancia, iteraciones, 0, request)
            df_seidel = MatJacobiSeid_CS2(A, b, x0, tolerancia, iteraciones, 1, request)
            df_sor2 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w2, request)
            df_sor3 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w3, request)
            if w:
                w = float(w)
            else:
                w = w1
            df_sor1 = SOR_CS2(A, b, x0, tolerancia, iteraciones, w, request)

        if metodo == "jacobi":
            solucion = df_jacobi.to_html(classes='table table-striped', index=False)
        elif metodo == "seidel":
            solucion = df_seidel.to_html(classes='table table-striped', index=False)
        elif metodo == "sor":
            solucion = df_sor1.to_html(classes='table table-striped', index=False)

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

    for nombre_metodo, df_metodo in metodos.items():
        ultima_fila = df_metodo.iloc[-1]
        nueva_fila = [nombre_metodo] + ultima_fila.tolist()
        tabla.loc[len(tabla)] = nueva_fila
    
    tabla = tabla.to_html(classes='table table-striped', index=False)

    return tabla
