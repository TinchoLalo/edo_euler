def euler_method(f, x0, y0, h, n):
    """
    Implementación del método de Euler para resolver una EDO de primer orden con valor inicial.
    
    Argumentos:
    f: Función que representa la ecuación diferencial dy/dx = f(x, y).
    x0: Valor inicial de x.
    y0: Valor inicial de y en x0.
    h: Tamaño del paso.
    n: Número de pasos.
    
    Retorna:
    Una lista de tuplas (xi, yi) que representan los valores aproximados de la solución en cada paso.
    """
    result = [(x0, y0)]
    xi = x0
    yi = y0
    for i in range(1, n+1):
        yi = yi + h * f(xi, yi)
        xi = xi + h
        result.append((xi, yi))
    return result



