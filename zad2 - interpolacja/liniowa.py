from tkinter import Tk, Canvas, Scale, HORIZONTAL, filedialog
from PIL import Image, ImageTk
import math
import tkinter as tk

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
    scaled_image = scale_linear(rotated_image, scale_factor)
    tk_rotated_image = ImageTk.PhotoImage(scaled_image)

    # Dostosuj rozmiar processed_canvas do rozmiaru przetworzonego obrazu
    processed_canvas.config(width=scaled_image.width, height=scaled_image.height)
    processed_canvas.create_image(scaled_image.width / 2, scaled_image.height / 2, image=tk_rotated_image)
    processed_canvas.image = tk_rotated_image

def scale_linear(img, scale_factor):
    width, height = img.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    new_img = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            # Oblicza współrzędne w oryginalnym obrazie
            orig_x = (x + 0.5) / scale_factor - 0.5
            orig_y = (y + 0.5) / scale_factor - 0.5

            # Pobiera współrzędne czterech najbliższych pikseli
            x0 = int(orig_x)
            x1 = min(x0 + 1, width - 1)
            y0 = int(orig_y)
            y1 = min(y0 + 1, height - 1)

            # Oblicza części pikseli
            p0 = img.getpixel((x0, y0))
            p1 = img.getpixel((x1, y0))
            p2 = img.getpixel((x0, y1))
            p3 = img.getpixel((x1, y1))

            # Oblicza wagi dla interpolacji
            fx1 = orig_x - x0
            fx0 = 1 - fx1
            fy1 = orig_y - y0
            fy0 = 1 - fy1

            # Oblicza interpolację liniową
            new_pixel = [0, 0, 0]
            for i in range(3):
                new_pixel[i] = (p0[i] * fx0 * fy0 + p1[i] * fx1 * fy0 +
                                p2[i] * fx0 * fy1 + p3[i] * fx1 * fy1)

            new_img.putpixel((x, y), tuple(map(int, new_pixel)))

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
root.title("Liniowa")

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