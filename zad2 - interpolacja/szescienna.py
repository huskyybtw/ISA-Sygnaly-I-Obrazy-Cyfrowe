import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def load_image():
    global original_image, tk_original_image
    file_path = filedialog.askopenfilename()
    original_image = Image.open(file_path)
    tk_original_image = ImageTk.PhotoImage(original_image)
    original_canvas.create_image(original_image.width / 2, original_image.height / 2, image=tk_original_image)
    original_canvas.image = tk_original_image
    update_image()  # Update the processed image view

def update_image():
    scale_factor = scale_slider.get()
    rotation_angle = rotation_slider.get()
    rotated_image = rotate_image(original_image, rotation_angle)
    scaled_image = scale_cubic(rotated_image, scale_factor)
    tk_rotated_image = ImageTk.PhotoImage(scaled_image)

    # Dostosuj rozmiar processed_canvas do rozmiaru przetworzonego obrazu
    processed_canvas.config(width=scaled_image.width, height=scaled_image.height)
    processed_canvas.create_image(scaled_image.width / 2, scaled_image.height / 2, image=tk_rotated_image)
    processed_canvas.image = tk_rotated_image

def cubic_interpolate(p0, p1, p2, p3, x):
    return p1 + 0.5 * x*(p2 - p0 + x*(2.0*p0 - 5.0*p1 + 4.0*p2 - p3 + x*(3.0*(p1 - p2) + p3 - p0)))

def get_pixel_value(img, x, y):
    if x < 0 or y < 0 or x >= img.width or y >= img.height:
        return 0, 0, 0
    else:
        return img.getpixel((int(x), int(y)))

def scale_cubic(img, scale_factor):
    width, height = img.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    new_img = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            gx = x / scale_factor
            gy = y / scale_factor
            gxi = int(gx)
            gyi = int(gy)

            # Pobiera wartości czterech najbliższych pikseli
            c0 = get_pixel_value(img, gxi - 1, gyi - 1)
            c1 = get_pixel_value(img, gxi, gyi - 1)
            c2 = get_pixel_value(img, gxi + 1, gyi - 1)
            c3 = get_pixel_value(img, gxi + 2, gyi - 1)
            row0 = cubic_interpolate(c0[0], c1[0], c2[0], c3[0], gx - gxi)

            c0 = get_pixel_value(img, gxi - 1, gyi)
            c1 = get_pixel_value(img, gxi, gyi)
            c2 = get_pixel_value(img, gxi + 1, gyi)
            c3 = get_pixel_value(img, gxi + 2, gyi)
            row1 = cubic_interpolate(c0[0], c1[0], c2[0], c3[0], gx - gxi)

            c0 = get_pixel_value(img, gxi - 1, gyi + 1)
            c1 = get_pixel_value(img, gxi, gyi + 1)
            c2 = get_pixel_value(img, gxi + 1, gyi + 1)
            c3 = get_pixel_value(img, gxi + 2, gyi + 1)
            row2 = cubic_interpolate(c0[0], c1[0], c2[0], c3[0], gx - gxi)

            c0 = get_pixel_value(img, gxi - 1, gyi + 2)
            c1 = get_pixel_value(img, gxi, gyi + 2)
            c2 = get_pixel_value(img, gxi + 1, gyi + 2)
            c3 = get_pixel_value(img, gxi + 2, gyi + 2)
            row3 = cubic_interpolate(c0[0], c1[0], c2[0], c3[0], gx - gxi)

            new_pixel = cubic_interpolate(row0, row1, row2, row3, gy - gyi)
            new_img.putpixel((x, y), (int(new_pixel), int(new_pixel), int(new_pixel)))

    return new_img


def rotate_image(img, angle):
    width, height = img.size
    new_img = Image.new("RGB", (width, height))
    angle = math.radians(angle)
    ox, oy = width / 2, height / 2

    for x in range(width):
        for y in range(height):
            tx = x - ox
            ty = y - oy
            new_x = ox + (tx * math.cos(angle) - ty * math.sin(angle))
            new_y = oy + (tx * math.sin(angle) + ty * math.cos(angle))
            if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
                new_img.putpixel((x, y), img.getpixel((int(new_x), int(new_y))))
            else:
                new_img.putpixel((x, y), (0, 0, 0))

    return new_img

# Create the main window
root = tk.Tk()
root.title("Szescienna")

# Create two Canvas widgets for original and processed images
original_canvas = tk.Canvas(root)
original_canvas.pack(side=tk.LEFT)

processed_canvas = tk.Canvas(root)
processed_canvas.pack(side=tk.RIGHT)

# Create sliders for scaling and rotation
scale_slider = tk.Scale(root, from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Scale", command=lambda val: update_image())
scale_slider.set(1)
scale_slider.pack()

rotation_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="Rotation", command=lambda val: update_image())
rotation_slider.pack()

# Load image button
load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack()

# Start the GUI event loop
root.mainloop()