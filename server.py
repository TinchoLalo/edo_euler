from flask import Flask, send_from_directory, request, jsonify # librerias necesarias para crear el servidor
from flask_cors import CORS # CORS
from sympy import symbols, sympify, lambdify # importamos una libreria para convertir cadenas en funciones
from euler_method import euler_method # importamos la funcion para resolver EDOs

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
port = 5000 # puerto donde va a correr el servidor

# Ruta principal donde cargamos el index.html (la página web)
@app.route("/")
def base():
    return send_from_directory('public', 'index.html')

# Nos permite cargar archivos estáticos (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('public', path)

# ========= EJERCICIO 1 =========
@app.route("/edo1/a", methods=['GET']) # definimos la ruta y el método
def edo1_a():
    # Funcion
    def f(x, y):
        return 0.2 * x * y
    # Valores iniciales
    x0 = 1
    y0 = 1

    # Paso de 0.1
    h = 0.1
    n = int((1.5 - x0) / h)  # Número de pasos necesario para llegar a x = 1.5

    # Resolver
    solution = euler_method(f, x0, y0, h, n)
    result = solution[-1][1]  # Aproximación de y(1.5) con paso de 0.1
    return jsonify({'result': result})

# ========= EJERCICIO 1B =========
@app.route("/edo1/b", methods=['GET'])
def edo1_b():
    # Funcion
    def f(x, y):
        return 0.2 * x * y
    
    # Valores iniciales
    x0 = 1
    y0 = 1

    # Paso de 0.05
    h = 0.05
    n = int((1.5 - x0) / h)  # Número de pasos necesario para llegar a x = 1.5

    # Resolver
    solution = euler_method(f, x0, y0, h, n)
    result = solution[-1][1]  # Aproximación de y(1.5) con paso de 0.05
    return jsonify({'result': result})

# ========= EJERCICIO 2 =========
@app.route("/edo2/a", methods=['GET'])
def edo2_a():
    # Valores dados en el problema
    R = 12  # Resistencia (Ohmios)
    L = 4   # Inductancia (Henrios)
    V = 60  # Voltaje de la batería (Voltios)
    I0 = 0  # Corriente inicial (A)
    # Funcion
    def f(x, y):
        return 15 - 3 * I0
    
    # Valores iniciales
    t = 0
    y0 = I0

    # Paso 
    h = 0.001 # paso del tiempo
    n = int(0.5 / h)  # Número de pasos para medio segundo

    # Resolver
    solution = euler_method(f, t, y0, h, n)
    result = solution[-1][1]  
    return jsonify({'result': result})


# ========= CALCULADORA =========
@app.route('/calculate', methods=['POST'])
def calculate():
    # recibimos los datos desde el frontend
    data = request.json
    edo = data['edo']
    x0 = data['targetX']
    y0 = data['initialValue']
    y = data['y']
    h = data['stepSize']
    n = int((y - x0) / h) 
    
    # convertimos la EDO que está en formato texto a una función algebráica
    x, y = symbols('x y')
    expr= sympify(edo)
    # Definir la función utilizando lambdify
    f = lambdify((x, y), expr)
    
    solution = euler_method(f, x0, y0, h, n)
    result = solution[-1][1]  # Último valor de la solución
    return jsonify({'result': result})



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
