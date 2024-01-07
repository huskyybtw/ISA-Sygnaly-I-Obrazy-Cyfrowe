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
    scaled_image = scale_nearest_neighbor(rotated_image, scale_factor)
    tk_rotated_image = ImageTk.PhotoImage(scaled_image)

    # Dostosuj rozmiar processed_canvas do rozmiaru przetworzonego obrazu
    processed_canvas.config(width=scaled_image.width, height=scaled_image.height)
    processed_canvas.create_image(scaled_image.width / 2, scaled_image.height / 2, image=tk_rotated_image)
    processed_canvas.image = tk_rotated_image

def scale_nearest_neighbor(img, scale_factor):
    width, height = img.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    new_img = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            orig_x = int(x / scale_factor)
            orig_y = int(y / scale_factor)
            new_img.putpixel((x, y), img.getpixel((orig_x, orig_y)))

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
root.title("Najblizszy sasiad")

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