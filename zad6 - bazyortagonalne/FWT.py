import pywt
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from skimage.color import rgb2gray


def rescale_image(image):
    image_min = image.min()
    image_max = image.max()
    return ((image - image_min) / (image_max - image_min) * 255).astype('uint8')


def process_image_with_wavelet(image_path, wavelet_name):
    # Wczytanie i konwersja obrazu na skalę szarości
    image = imread(image_path)
    if len(image.shape) == 3:
        image = rgb2gray(image)

    # Dekompozycja falkowa
    coeffs2 = pywt.dwt2(image, wavelet_name)
    cA, (cH, cV, cD) = coeffs2

    # Rekonstrukcja obrazu z wykorzystaniem tylko współczynnika przybliżenia
    reconstructed_image = pywt.idwt2((cA, (None, None, None)), wavelet_name)

    # Przeskalowanie obrazu do formatu uint8
    reconstructed_image = rescale_image(reconstructed_image)

    # Wyświetlanie obrazu oryginalnego i przetworzonego
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(reconstructed_image, cmap='gray')
    plt.title(f'Reconstructed Image with {wavelet_name}')
    plt.axis('off')

    plt.show()

    # Zapisywanie przetworzonego obrazu
    save_path = f'reconstructed_{wavelet_name}.png'
    imsave(save_path, reconstructed_image)

    return reconstructed_image


# Parametry
image_path = 'obrazy/lambda_0.00.png'  # Ścieżka do obrazu
wavelet_names = ['haar', 'bior3.5', 'bior6.8']


for wavelet_name in wavelet_names:
    print(f"Processing with wavelet: {wavelet_name}")
    process_image_with_wavelet(image_path, wavelet_name)
