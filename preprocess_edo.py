import re

""" 
Función para preprocesar la EDO ingresada por el usuario. De esta forma se asegura que la EDO sea correcta y pueda ser resuelta con el Método de Euler.
"""

def preprocess_edo(edo):
    # Eliminar "y' = " de la ecuación
    edo = re.sub(r"y\s*'?\s*=\s*", "", edo)

    # Eliminar "y'(x) = " de la ecuación
    edo = re.sub(r"y'\s*\(\s*x\s*\)\s*'?\s*=\s*", "", edo)

    # Eliminar si se ingresa como "dy/dx = " de la ecuación
    edo = re.sub(r"dy/dx\s*'?\s*=\s*", "", edo)

    # Cambiar "^" a "**" para potencias
    edo = edo.replace("^", "**")

    # Lista de funciones matemáticas que deben tener paréntesis
    func_pattern = r'(sin|cos|tan|exp|log|abs|sqrt|sinh|cosh|tanh|arcsin|arccos|arctan|ln)(\s*\(?)'
    
    # Asegurar que las funciones tengan paréntesis y argumentos válidos
    def add_parentheses(match):
        func = match.group(1)
        if match.group(0).endswith('('):
            return func + '('
        return func + '('

    edo = re.sub(func_pattern, add_parentheses, edo)

    # Multiplicaciónes 
    # Entre número y 'x' o 'y' (ej: 2x → 2*x, 3y → 3*y)
    edo = re.sub(r'(?<=\d)(?=[xy])', '*', edo)

    # Entre 'x' e 'y' o 'y' e 'x' (ej: xy → x*y, yx → y*x)
    edo = re.sub(r'(?<=x)(?=y)|(?<=y)(?=x)', '*', edo)
    
    # Entre x o y e cos, sin, etc. (ej: xcos(x) → x*cos(x))
    edo = re.sub(r'(?<=x|y)\s*(?=[a-zA-Z])', '*', edo)

    # Cerrar paréntesis abiertos por funciones si no están cerrados
    open_parens = edo.count('(')
    close_parens = edo.count(')')
    if open_parens > close_parens:
        edo += ')' * (open_parens - close_parens)

    return edo