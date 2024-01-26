import numpy as np
from skimage import io

def calculate_mse(image1, image2):
    """Oblicza Mean Squared Error między dwoma obrazami."""
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])

    return err


def calculate_mae(image1, image2):
    """Oblicza Mean Absolute Error między dwoma obrazami."""
    err = np.sum(abs(image1.astype("float") - image2.astype("float")))
    err /= float(image1.shape[0] * image1.shape[1])

    return err

# Wczytaj dwa obrazy
image1 = io.imread('obraz.jpg')
image2 = io.imread('processed_images/lambda_128_cubic_resized_2048x2048_rotated_0_cubic_resized_1024x1024_rotated_0.png')

# Upewnij się, że obrazy mają tę samą wielkość
if image1.shape != image2.shape:
    raise ValueError("Obrazy muszą mieć takie same wymiary")

# Oblicz MSE i MAE
mse = calculate_mse(image1, image2)
mae = calculate_mae(image1, image2)

print(f"MSE: {mse:.6f}")
print(f"MAE: {mae:.6f}")
