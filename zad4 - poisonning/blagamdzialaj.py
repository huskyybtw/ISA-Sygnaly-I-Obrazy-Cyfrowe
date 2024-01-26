import cv2
import os
import time

# Parametry
file_path = 'processed_images/lambda_128_nearest_resized_2048x2048_rotated_0.png'
interpolation_method = cv2.INTER_NEAREST
target_size = (1024, 1024)
rotation_angle = 0

def get_interpolation_method_name(interpolation_method):
    if interpolation_method == cv2.INTER_LINEAR:
        return 'linear'
    elif interpolation_method == cv2.INTER_NEAREST:
        return 'nearest'
    elif interpolation_method == cv2.INTER_CUBIC:
        return 'cubic'
    elif interpolation_method == cv2.INTER_AREA:
        return 'area'
    else:
        return 'unknown'

def format_output_filename(base_name, interpolation_method, target_size, rotation_angle):
    name, ext = os.path.splitext(os.path.basename(base_name))
    interpolation_method_name = get_interpolation_method_name(interpolation_method)
    return f"{name}_{interpolation_method_name}_resized_{target_size[0]}x{target_size[1]}_rotated_{rotation_angle}{ext}"

def process_image(file_path, interpolation_method, target_size, rotation_angle):
    # Folder do zapisywania obrazów
    OUTPUT_FOLDER = 'processed_images'

    # Tworzenie folderu do zapisywania obrazów, jeśli nie istnieje
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Wczytaj obraz
    original_image = cv2.imread(file_path)

    # Pomiar czasu dla skalowania obrazu
    start_scale_time = time.time()
    resized_image = cv2.resize(original_image, target_size, interpolation=interpolation_method)
    end_scale_time = time.time()
    print(f"Czas skalowania: {end_scale_time - start_scale_time:.8f} sekund")

    # Pomiar czasu dla obrotu obrazu
    start_rotate_time = time.time()
    M = cv2.getRotationMatrix2D((target_size[0] // 2, target_size[1] // 2), rotation_angle, 1)
    rotated_image = cv2.warpAffine(resized_image, M, target_size)
    end_rotate_time = time.time()
    print(f"Czas obrotu: {end_rotate_time - start_rotate_time:.5f} sekund")

    # Zapisz przetworzony obraz z sformatowaną nazwą
    output_file_name = format_output_filename(file_path, interpolation_method, target_size, rotation_angle)
    output_file_path = os.path.join(OUTPUT_FOLDER, output_file_name)
    cv2.imwrite(output_file_path, rotated_image)
    print(f"Przetworzony obraz został zapisany w: {output_file_path}")

process_image(file_path, interpolation_method, target_size, rotation_angle)
