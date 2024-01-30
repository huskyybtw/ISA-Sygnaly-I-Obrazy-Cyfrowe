import numpy as np
import matplotlib.pyplot as plt

def sample_function_1d(func, K):
    x = np.linspace(-2, 2, K)  # Przykładowy zakres próbkowania
    return x, func(x)

# Funkcje interpolujące
def pi_function(x):
    return np.sinc(x)

def lambda_function(x):
    return np.maximum(1 - np.abs(x), 0)

def omega_function(x):
    return np.exp(-x**2)

K = 100
x_pi, sampled_pi = sample_function_1d(pi_function, K)
x_lambda, sampled_lambda = sample_function_1d(lambda_function, K)
x_omega, sampled_omega = sample_function_1d(omega_function, K)

# Wizualizacja
plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.plot(x_pi, sampled_pi)
plt.title("Π Function")
plt.subplot(132)
plt.plot(x_lambda, sampled_lambda)
plt.title("Λ Function")
plt.subplot(133)
plt.plot(x_omega, sampled_omega)
plt.title("Ω Function")
plt.show()

def sample_function_2d(func, K):
    x = np.linspace(-2, 2, K)
    xx, yy = np.meshgrid(x, x)
    return func(xx) * func(yy)

# Próbkowanie i wizualizacja 2D
sampled_pi_2d = sample_function_2d(pi_function, K)
sampled_lambda_2d = sample_function_2d(lambda_function, K)
sampled_omega_2d = sample_function_2d(omega_function, K)

plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.imshow(sampled_pi_2d, cmap='gray', interpolation='nearest')
plt.title("Π Function 2D")
plt.colorbar()
plt.subplot(132)
plt.imshow(sampled_lambda_2d, cmap='gray', interpolation='nearest')
plt.title("Λ Function 2D")
plt.colorbar()
plt.subplot(133)
plt.imshow(sampled_omega_2d, cmap='gray', interpolation='nearest')
plt.title("Ω Function 2D")
plt.colorbar()
plt.show()
