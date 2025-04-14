from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from .biseccion import biseccion_CS, biseccion_DC
from .regla_falsa import regla_falsa_CS, regla_falsa_DC
from .punto_fijo import punto_fijo_CS, punto_fijo_DC
from .newton import newton_CS, newton_DC
from .secante import secante_CS, secante_DC
from .raices_multiples import newton_m2_CS, newton_m2_DC

def inicio(request):
    df = None
    grafico = None
    reporte = None

    if request.method == "POST":
        formulario = request.POST.get("formulario")

        if formulario == "enl":
            print("antes de")
            df, grafico = enl(request)
            print(df)
            return render(request, 'inicio.html', {'tabla': df, 'grafico': grafico, 'reporte': reporte, 'formulario_activo': formulario})

        elif formulario == "reporte_enl":
            df, reporte = reporte_enl(request)
            return render(request, 'inicio.html', {'tabla': df, 'grafico': grafico, 'reporte': reporte, 'formulario_activo': formulario})
    
    return render(request, 'inicio.html', {'tabla': df, 'grafico': grafico, 'reporte': reporte, 'formulario_activo': "enl"})

def enl(request):
    print("adentro")
    metodo = request.POST.get("metodo")
    tipo_error = request.POST.get("tipo_error")  # 'DC' o 'CS'
    tolerancia = request.POST.get("tolerancia")
    fx = request.POST.get("funcion")
    iteraciones = int(request.POST.get("iteraciones"))
    print("ya se hizo lo inicial")

    # Nombre dinámico de la función, ej: biseccion_DC
    nombre_funcion = f"{metodo.lower().replace(' ', '_')}_{tipo_error}"
    print(nombre_funcion)

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
        
        return df, grafico

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None
    
def reporte_enl(request):
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
        tabla, reporte = entregar_solucion(soluciones, iteraciones)
        return tabla, reporte

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return None, None
    
def hallar_mejor_metodo(df_bis, df_rf, df_pf, df_newton, df_secante, df_rm):
    soluciones = [df_bis, df_rf, df_pf, df_newton, df_secante, df_rm]
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

def crear_reporte(df_bis, df_rf, df_pf, df_newton, df_secante, df_rm, mejor_metodo):
    if mejor_metodo is df_bis:
        nombre_metodo = "método de la bisección"
    elif mejor_metodo is df_rf:
        nombre_metodo = "método de la regla falsa"
    elif mejor_metodo is df_pf:
        nombre_metodo = "método de punto fijo"
    elif mejor_metodo is df_newton:
        nombre_metodo = "método de Newton"
    elif mejor_metodo is df_secante:
        nombre_metodo = "método de la secante"
    elif mejor_metodo is df_rm:
        nombre_metodo = "método de raíces múltiples"

    reporte = f"""
        <div>
            <ul>
                <li>
                    Bisección: iteraciones -> {df_bis.iloc[-1, 0]}; error -> {df_bis.iloc[-1, 3]}
                </li>
                <li>
                    Regla Falsa: iteraciones -> {df_rf.iloc[-1, 0]}; error -> {df_rf.iloc[-1, 3]}
                </li>
                <li>
                    Punto Fijo: iteraciones -> {df_pf.iloc[-1, 0]}; error -> {df_pf.iloc[-1, 3]}
                </li>
                <li>
                    Newton: iteraciones -> {df_newton.iloc[-1, 0]}; error -> {df_newton.iloc[-1, 3]}
                </li>
                <li>
                    Secante: iteraciones -> {df_secante.iloc[-1, 0]}; error -> {df_secante.iloc[-1, 3]}
                </li>
                <li>
                    Raíces Múltiples: iteraciones -> {df_rm.iloc[-1, 0]}; error -> {df_rm.iloc[-1, 3]}
                </li>
            </ul>
            <p>El mejor método fue el {nombre_metodo}, requiriendo {mejor_metodo.iloc[-1, 0]} iteraciones y con un error de {mejor_metodo.iloc[-1, 3]}.</p>
        </div>
    """
    return reporte

def entregar_solucion(soluciones, iteraciones):
    i = 0
    for metodo in soluciones:
        if type(metodo) == str:
            soluciones[i] = pd.read_html(metodo)[0]
        else:
            soluciones[i] = pd.DataFrame(data={'iter': [iteraciones], 'X': [None], 'f(X)': [None], 'E': [1]})
        i += 1

    mejor_metodo = hallar_mejor_metodo(soluciones[0], soluciones[1], soluciones[2], soluciones[3], soluciones[4], soluciones[5])

    reporte = crear_reporte(soluciones[0], soluciones[1], soluciones[2], soluciones[3], soluciones[4], soluciones[5], mejor_metodo)

    tabla = mejor_metodo.to_html(classes='table table-striped', index=False)

    return tabla, reporte