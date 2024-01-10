import cv2
import time
import numpy as np
import os

# Stałe dla skalowania i obrotu
SCALE_FACTOR = 1.5
ROTATION_ANGLE = 24

# Typ interpolacji
INTERPOLATION_METHOD = cv2.INTER_LINEAR

# Folder do zapisywania obrazów
OUTPUT_FOLDER = 'processed_images'

def calculate_mse(original, processed):
    return np.mean((original - processed) ** 2)

def calculate_mae(original, processed):
    return np.mean(np.abs(original - processed))

def process_image(file_path, interpolation_method):
    # Wczytaj obraz
    original_image = cv2.imread(file_path)
    image = original_image.copy()

    # Skalowanie obrazu
    start_scale_time = time.time()
    scaled_image = cv2.resize(image, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR, interpolation=interpolation_method)
    end_scale_time = time.time()
    scale_time = end_scale_time - start_scale_time
    print(f"Czas skalowania: {scale_time:.5} sekund")

    # Obrót obrazu
    start_rotate_time = time.time()
    M = cv2.getRotationMatrix2D((scaled_image.shape[1] // 2, scaled_image.shape[0] // 2), ROTATION_ANGLE, 1)
    processed_image = cv2.warpAffine(scaled_image, M, (scaled_image.shape[1], scaled_image.shape[0]), flags=interpolation_method)
    end_rotate_time = time.time()
    rotate_time = end_rotate_time - start_rotate_time
    print(f"Czas obrotu: {rotate_time:.5} sekund")

    # Obliczanie MSE i MAE
    resized_processed_image = cv2.resize(processed_image, (original_image.shape[1], original_image.shape[0]), interpolation=interpolation_method)
    mse = calculate_mse(original_image, resized_processed_image)
    mae = calculate_mae(original_image, resized_processed_image)
    print(f"MSE: {mse}, MAE: {mae}")

    # Tworzenie folderu do zapisywania obrazów, jeśli nie istnieje
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Zapisz oryginalny obraz
    original_output_path = os.path.join(OUTPUT_FOLDER, 'original2.jpg')
    cv2.imwrite(original_output_path, original_image)
    print(f"Oryginalny obraz został zapisany do: {original_output_path}")

    # Zapisz przetworzony obraz
    interpolation_name = {cv2.INTER_LINEAR: 'linear', cv2.INTER_CUBIC: 'cubic', cv2.INTER_NEAREST: 'nearest'}.get(interpolation_method, 'unknown')
    processed_output_filename = f"processed_{interpolation_name}_scale_{SCALE_FACTOR}_rot_{ROTATION_ANGLE}.jpg"
    processed_output_path = os.path.join(OUTPUT_FOLDER, processed_output_filename)
    cv2.imwrite(processed_output_path, processed_image)
    print(f"Przetworzony obraz został zapisany do: {processed_output_path}")

file_path = 'pobrane.jpg'
process_image(file_path, INTERPOLATION_METHOD)
