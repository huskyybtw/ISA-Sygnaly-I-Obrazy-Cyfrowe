import numpy as np
from scipy.linalg import hadamard
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

def wht2(img):
    H = hadamard(img.shape[0])
    return np.dot(np.dot(H, img), H)

def iwht2(img):
    H = hadamard(img.shape[0])
    return np.dot(np.dot(H, img), H) / (img.shape[0] ** 2)

def threshold(data, T):
    return np.where(abs(data) > T, data, 0)

def quantize(data, Q):
    return np.round(data / Q) * Q

def rescale_image(image):
    image_min = image.min()
    image_max = image.max()
    return ((image - image_min) / (image_max - image_min) * 255).astype('uint8')

def count_nonzero_coefficients(image):
    return np.count_nonzero(image)

def process_wht_image(image_path, T, Q):
    # Wczytanie obrazu
    image = imread(image_path, as_gray=True)
    if image.ndim == 3:
        image = rgb2gray(image)

    # Transformacja WHT
    wht_coeffs = wht2(image)

    # Progowanie i kwantyzacja
    wht_thresh = threshold(wht_coeffs, T)
    wht_quant = quantize(wht_thresh, Q)

    # Odwrotna transformacja WHT
    reconstructed = iwht2(wht_quant)

    # Wyświetlanie obrazów
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(reconstructed, cmap='gray')
    plt.title('Reconstructed Image')
    plt.axis('off')

    plt.show()

    return rescale_image(reconstructed)

# Parametry
T = 0.6  # Prog
Q = 512   # Ziarno kwantyzacji
image_path = 'obrazy/lambda_0.00.png'  # Ścieżka do obrazu
reconstructed = process_wht_image(image_path, T, Q)

# Zapisywanie przetworzonego obrazu
save_path = f'obrazy/walsha_T_{T:.2f}_Q_{Q}.png'
imsave(save_path, reconstructed)

