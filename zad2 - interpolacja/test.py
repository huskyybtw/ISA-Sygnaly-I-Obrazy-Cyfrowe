import cv2
import time
import os

# Stałe dla skalowania i obrotu
SCALE_FACTOR = 1.5  # Przykładowa wartość, możesz ją zmienić
ROTATION_ANGLE = 0 # Przykładowa wartość, możesz ją zmienić

# Typ interpolacji: cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_NEAREST
INTERPOLATION_METHOD = cv2.INTER_NEAREST

# Folder do zapisywania obrazów
OUTPUT_FOLDER = 'processed_images'

def process_image(file_path, interpolation_method):
    # Wczytaj obraz
    image = cv2.imread(file_path)

    # Rozpocznij pomiar czasu
    start_time = time.time()

    # Skalowanie i obrót obrazu
    scaled_image = cv2.resize(image, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR, interpolation=interpolation_method)
    M = cv2.getRotationMatrix2D((scaled_image.shape[1] // 2, scaled_image.shape[0] // 2), ROTATION_ANGLE, 1)
    processed_image = cv2.warpAffine(scaled_image, M, (scaled_image.shape[1], scaled_image.shape[0]), flags=interpolation_method)

    # Zakończ pomiar czasu
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Czas przetwarzania: {processing_time:.5} sekund")

    # Zapisz przetworzony obraz
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    interpolation_name = {cv2.INTER_LINEAR: 'linear', cv2.INTER_CUBIC: 'cubic', cv2.INTER_NEAREST: 'nearest'}.get(interpolation_method, 'unknown')
    output_filename = f"processed_{interpolation_name}_scale_{SCALE_FACTOR}_rot_{ROTATION_ANGLE}.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    cv2.imwrite(output_path, processed_image)
    print(f"Obraz został zapisany do: {output_path}")

# Ścieżka do twojego obrazu
file_path = 'pobrane.jpg'  # Zmień na ścieżkę do swojego obrazu
process_image(file_path, INTERPOLATION_METHOD)
