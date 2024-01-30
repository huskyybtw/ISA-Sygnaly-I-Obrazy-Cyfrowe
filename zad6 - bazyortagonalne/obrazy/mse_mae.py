import numpy as np
from skimage import io, color

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

def convert_to_gray_and_resize(image):
    """Konwertuje obraz na skalę szarości i dostosowuje rozmiar."""
    if len(image.shape) == 3:
        image = color.rgb2gray(image)
    return image

# Wczytaj dwa obrazy
image1 = io.imread('drugi.png')
image2 = io.imread('reconstructed_bior6.8.png')

# Konwersja obrazów do skali szarości
image1 = convert_to_gray_and_resize(image1)
image2 = convert_to_gray_and_resize(image2)

# Upewnij się, że obrazy mają tę samą wielkość
if image1.shape != image2.shape:
    raise ValueError("Obrazy muszą mieć takie same wymiary")

# Oblicz MSE i MAE
mse = calculate_mse(image1, image2)
mae = calculate_mae(image1, image2)

print(f"MSE: {mse:.6f}")
print(f"MAE: {mae:.6f}")
