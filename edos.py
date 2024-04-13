from euler_method import euler_method

# Ejemplo de uso:
def f(x, y):
    return 0.2 * x * y
def f2(x, y):
    return y
# Valores iniciales
x0 = 1
y0 = 1
x1 = 0

# Paso de 0.1
h1 = 0.1
n1 = int((1.5 - x0) / h1)  # Número de pasos necesario para llegar a x = 1.5

# Paso de 0.05
h2 = 0.05
n2 = int((1.5 - x0) / h2)  # Número de pasos necesario para llegar a x = 1.5

# Resolver con paso de 0.1
solution1 = euler_method(f, x0, y0, h1, n1)
approximation1 = solution1[-1][1]  # Aproximación de y(1.5) con paso de 0.1

# Resolver con paso de 0.05
solution2 = euler_method(f, x0, y0, h2, n2)
approximation2 = solution2[-1][1]  # Aproximación de y(1.5) con paso de 0.05

n3 = int((1 - 0) / 0.1)  # Número de pasos necesario para llegar a x = 1

solution3 = euler_method(f, 0, y0, 0.1, n3)
approximation3 = solution3[-1][1]  # Aproximación de y(1.5) con paso de 0.05

# Imprimir resultados
print("Aproximación de y(1.5) con paso de 0.1:", approximation1)
print("Aproximación de y(1.5) con paso de 0.05:", approximation2)

print("Aproximación de y(1) con paso de 0.1:", approximation3)

