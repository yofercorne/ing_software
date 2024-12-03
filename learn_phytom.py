import numpy as np

# Definir la función f'(x)
def f_prime(x):
    return 0.5 * (np.exp(x / 1.24) - np.exp(-x / 1.24))

# Definir la función integranda g(x)
def g(x):
    return np.sqrt(1 + (f_prime(x))**2)

# Intervalo y número de subintervalos
a, b = -1.2, 1.2
n = 4
h = (b - a) / n

# Puntos donde se evalúa
x = np.linspace(a, b, n + 1)
g_values = g(x)

# Aplicar la fórmula de Simpson
print("h:",h)
print("g_values:",g_values[0])
print("g_X:",g(-1.2))

print("4 * sum(g_values[1:-1:2]):",4 * sum(g_values[1:-1:2]))


L = (h / 3) * (g_values[0] + 4 * sum(g_values[1:-1:2]) + 2 * sum(g_values[2:-1:2]) + g_values[-1])

print(L)
