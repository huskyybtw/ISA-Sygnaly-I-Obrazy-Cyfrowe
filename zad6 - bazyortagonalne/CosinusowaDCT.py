from scipy.fftpack import dct, idct
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import cv2
from skimage.color import rgb2gray

def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')

def threshold_and_quantize(coeffs, T, Q):
    thresholded = np.where(abs(coeffs) > T, coeffs, 0)
    quantized = np.round(thresholded / Q) * Q
    return quantized

def rescale_image(image):
    # Normalizuje obraz do zakresu 0-1, a następnie skaluje do zakresu 0-255
    image_min = image.min()
    image_max = image.max()
    return ((image - image_min) / (image_max - image_min) * 255).astype('uint8')

# Prog T i ziarno kwantyzacji Q
T = 0.1  # Przykładowy próg
Q = 32  # Przykładowe ziarno kwantyzacji

# Wczytanie obrazu
image_path = 'obrazy/lambda_0.00.png'
image = imread(image_path, as_gray=True)

# DCT
dct_coeffs = dct2(image)

# Progowanie i kwantyzacja
processed_coeffs = threshold_and_quantize(dct_coeffs, T, Q)

# IDCT
reconstructed_image = idct2(processed_coeffs)

# Przeskalowanie obrazu do zakresu 0-255
reconstructed_image = rescale_image(reconstructed_image)

# Wyświetlanie obrazów
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Noisy Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(reconstructed_image, cmap='gray')
plt.title('Reconstructed Image')
plt.axis('off')

plt.show()

# Zapisywanie przetworzonego obrazu
save_path = 'obrazy/cos.png'
cv2.imwrite(save_path, reconstructed_image)
