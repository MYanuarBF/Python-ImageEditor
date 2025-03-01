import tkinter as tk
import cv2
import numpy as np
from tkinter import filedialog, Scale
from PIL import Image, ImageTk

original_image = None

# fungsi fungsi
def open_image():
    global original_image
    file_path = filedialog.askopenfilename()
    original_image = cv2.imread(file_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    display_image(original_image)

def apply_filter(filter_name):
    global original_image
    if filter_name == "Median Blur":
        original_image = cv2.medianBlur(original_image, 5)
    elif filter_name == "Gaussian Blur":
        original_image = cv2.GaussianBlur(original_image, (5, 5), 0)
    elif filter_name == "Bilateral Filter":
        original_image = cv2.bilateralFilter(original_image, 9, 75, 75)
    display_image(original_image)

def rotate_image(angle):
    global original_image
    rows, cols = original_image.shape[0], original_image.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    original_image = cv2.warpAffine(original_image, M, (cols, rows))
    display_image(original_image)

def translate_image(tx, ty):
    global original_image
    rows, cols = original_image.shape[0], original_image.shape[1]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    original_image = cv2.warpAffine(original_image, M, (cols, rows))
    display_image(original_image)

def resize_image(width, height):
    global original_image
    original_image = cv2.resize(original_image, (width, height), interpolation=cv2.INTER_CUBIC)
    display_image(original_image)

def grayscale_image():
    global original_image
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # Make it 3-channel if it's grayscale to ensure compatibility for future operations
    if len(original_image.shape) == 2:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)
    display_image(original_image)

def invert_image():
    global original_image
    original_image = cv2.bitwise_not(original_image)
    display_image(original_image)

def save_image():
    global original_image
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("All Files", "*.*")])
    if filename:
        cv2.imwrite(filename, original_image)

def display_image(image):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    image_label.config(image=image)
    image_label.image = image

root = tk.Tk()
root.title("UAS Pengolahan Citra")

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.grid(row=0,column=0)
save_button = tk.Button(root, text="Save", command=save_image)
save_button.grid(row=0,column=1)

median_blur_button = tk.Button(root, text="Median Blur", command=lambda: apply_filter("Median Blur"))
median_blur_button.grid(row=1,column=0)

gaussian_blur_button = tk.Button(root, text="Gaussian Blur", command=lambda: apply_filter("Gaussian Blur"))
gaussian_blur_button.grid(row=1,column=1)

bilateral_filter_button = tk.Button(root, text="Bilateral Filter", command=lambda: apply_filter("Bilateral Filter"))
bilateral_filter_button.grid(row=1,column=2)

grayscale_button = tk.Button(root, text="Grayscale", command=grayscale_image)
grayscale_button.grid(row=1,column=3)

invert_button = tk.Button(root, text="Invert", command=invert_image)
invert_button.grid(row=1,column=4)

rotate_0_button = tk.Button(root, text="0°", command=lambda: rotate_image(0))
rotate_0_button.grid(row=2,column=0)

rotate_90_button = tk.Button(root, text="90°", command=lambda: rotate_image(90))
rotate_90_button.grid(row=2,column=1)

rotate_180_button = tk.Button(root, text="180°", command=lambda: rotate_image(180))
rotate_180_button.grid(row=2,column=2)

rotate_270_button = tk.Button(root, text="270°", command=lambda: rotate_image(270))
rotate_270_button.grid(row=2,column=3)

tx_slider = Scale(root, from_=-255, to=255, orient="horizontal", label="sumbu x")
tx_slider.grid(row=3,column=0)

ty_slider = Scale(root, from_=-255, to=255, orient="horizontal", label="sumbu y")
ty_slider.grid(row=3,column=1)

apply_translation_button = tk.Button(root, text="Apply Translation", command=lambda: translate_image(tx_slider.get(), ty_slider.get()))
apply_translation_button.grid(row=3,column=2)

width_entry = tk.Entry(root,textvariable="width")
width_entry.grid(row=4,column=0)

height_entry = tk.Entry(root)
height_entry.grid(row=4,column=1)

resize_button = tk.Button(root, text="Resize", command=lambda: resize_image(int(width_entry.get()), int(height_entry.get())))
resize_button.grid(row=4,column=2)


image_label = tk.Label(root)
image_label.grid(row=0,column=5,rowspan=5)

root.mainloop()
