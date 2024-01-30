import numpy as np
import cv2

def create_kernel(size, rodzaj):
    if size % 2 == 0:
        raise ValueError("Only odd integers are allowed")
    else:
        if rodzaj == "Gaussian":
            if size == 3:
                return np.array([[1, 2, 1],
                                 [2, 4, 2],
                                 [1, 2, 1]]) / 16
            elif size == 5:
                return np.array([[1, 4,  6, 4, 1],
                                 [4, 16, 24, 16, 4],
                                 [6, 24, 36, 24, 6],
                                 [4, 16, 24, 16, 4],
                                 [1, 4,  6, 4, 1]]) / 256
        elif rodzaj == "Box":
            return np.ones((size, size)) / (size * size)

def median_filtr(img, kernel_size):
    return cv2.medianBlur(img, kernel_size)

def splot_filtr(img, kernel):
    return cv2.filter2D(img, -1, kernel)

def apply_filters(image):
    kernel_sizes = [3,5]  # Przykładowe rozmiary jądra

    for kernel_size in kernel_sizes:
        # Wygładzanie za pomocą filtru medianowego
        median_filtered = median_filtr(image, kernel_size)
        cv2.imwrite(f"Wyniki_median_filtered_{kernel_size}.png", median_filtered)

        # Wygładzanie za pomocą filtru Gaussowskiego
        gaussian_kernel = create_kernel(kernel_size, "Gaussian")
        gaussian_filtered = splot_filtr(image, gaussian_kernel)
        cv2.imwrite(f"Wyniki_gaussian_filtered_{kernel_size}.png", gaussian_filtered)

# Załadowanie obrazu
working_image = cv2.imread("lambda_64.png")  # Podmień na ścieżkę do swojego obrazu

# Zastosowanie filtrów
apply_filters(working_image)
