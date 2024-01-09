import cv2
import numpy as np
import time

def resize_image(image, size, interpolation):
    return cv2.resize(image, size, interpolation=interpolation)

def calculate_mse(image1, image2):
    return np.mean((image1 - image2) ** 2)

def calculate_mae(image1, image2):
    return np.mean(np.abs(image1 - image2))
import cv2
import numpy as np
import time

def resize_image(image, size, interpolation):
    return cv2.resize(image, size, interpolation=interpolation)

def calculate_mse(image1, image2):
    return np.mean((image1 - image2) ** 2)

def calculate_mae(image1, image2):
    return np.mean(np.abs(image1 - image2))

# Konfiguracja
new_size = (100, 100) # Nowy rozmiar
interpolation_method = cv2.INTER_LINEAR # Wybierz metodę interpolacji
image_path = 'modified_image_lambda_1.png' # Ścieżka do obrazu

# Wczytanie obrazu
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Pomniejszenie obrazu
start_time = time.time()
resized_image = resize_image(original_image, new_size, interpolation_method)
shrink_time = time.time() - start_time

# Zapisz pomniejszony obraz
cv2.imwrite('resized_image.png', resized_image)

# Powiększenie obrazu do oryginalnego rozmiaru
start_time = time.time()
resized_up = resize_image(resized_image, original_image.shape[:2][::-1], interpolation_method)
up_time = time.time() - start_time

# Zapisz powiększony obraz
cv2.imwrite('resized_up_image.png', resized_up)

# Obliczanie MSE i MAE
mse = calculate_mse(original_image, resized_up)
mae = calculate_mae(original_image, resized_up)

print(f"MSE: {mse:.10f}, "
      f"MAE: {mae:.10f}, "
      f"Czas zmniejszania: {shrink_time:.10f} sekund, "
      f"Czas zwiekszania: {up_time:.10f} sekund")
