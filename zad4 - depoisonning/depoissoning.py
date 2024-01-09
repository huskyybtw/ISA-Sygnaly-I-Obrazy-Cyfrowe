import numpy as np
from scipy.stats import poisson
from PIL import Image
import os

image_path = 'obraz.jpg'
original_image = Image.open(image_path).convert('L')

lambda_values = [256,260,265,275]

# Funkcja do modyfikowania obrazu zgodnie z rozkładem Poissona
def apply_poisson_noise(image, lambda_value):
    image_array = np.array(image)
    noisy_image = poisson(lambda_value * image_array / 255.0).rvs() * 255 / lambda_value
    noisy_image = np.clip(noisy_image, 0, 255)
    return Image.fromarray(noisy_image.astype(np.uint8))

def save_image(image, lambda_value, folder):
    file_name = f'modified_image_lambda_{lambda_value}.png'
    image.save(os.path.join(folder, file_name))

# Generowanie i zapisywanie wersji obrazów
modified_images = []
folder_path = 'ścieżka_do_folderu'
os.makedirs(folder_path, exist_ok=True)  # Tworzenie folderu, jeśli nie istnieje

for lambda_value in lambda_values:
    modified_image = apply_poisson_noise(original_image, lambda_value)
    modified_images.append(modified_image)
    save_image(modified_image, lambda_value, folder_path)
