import cv2
import time
import os

# Stałe dla skalowania i obrotu
SCALE_FACTOR = 3  # Przykładowa wartość, możesz ją zmienić
ROTATION_ANGLE = 0  # Przykładowa wartość, możesz ją zmienić

# Folder do zapisywania obrazów
OUTPUT_FOLDER = 'processed_images'

def process_and_concatenate_images(file_path):
    # Wczytaj obraz
    image = cv2.imread(file_path)
    processed_images = []

    # Lista metod interpolacji
    interpolation_methods = [cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_NEAREST]

    for method in interpolation_methods:
        # Skalowanie i obrót obrazu
        scaled_image = cv2.resize(image, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR, interpolation=method)
        M = cv2.getRotationMatrix2D((scaled_image.shape[1] // 2, scaled_image.shape[0] // 2), ROTATION_ANGLE, 1)
        processed_image = cv2.warpAffine(scaled_image, M, (scaled_image.shape[1], scaled_image.shape[0]), flags=method)
        processed_images.append(processed_image)

    # Sklejanie obrazów w jeden
    concatenated_image = cv2.hconcat(processed_images)

    # Zapisz połączony obraz
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    output_path = os.path.join(OUTPUT_FOLDER, 'concatenated_image.jpg')
    cv2.imwrite(output_path, concatenated_image)
    print(f"Połączony obraz został zapisany do: {output_path}")

# Ścieżka do twojego obrazu
file_path = 'pobrane.jpg'  # Zmień na ścieżkę do swojego obrazu
process_and_concatenate_images(file_path)
