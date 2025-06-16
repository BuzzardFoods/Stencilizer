import cv2
import numpy as np
from tkinter import Tk, filedialog, Scale, Button, Label, IntVar, Checkbutton, Frame
from PIL import Image, ImageTk
import os

current_image_path = None

def load_image():
    global current_image_path
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if filepath:
        current_image_path = filepath
        update_preview()

def update_preview(event=None):
    if current_image_path:
        img = cv2.imread(current_image_path)
        if img is None:
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, threshold1.get(), threshold2.get())
        kernel = np.ones((spread.get(), spread.get()), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)

        if invert.get():
            dilated = cv2.bitwise_not(dilated)

        height, width = dilated.shape
        new_w = resolution.get()
        new_h = int((new_w / width) * height)
        resized_stencil = cv2.resize(dilated, (new_w, new_h), interpolation=cv2.INTER_AREA)

        if overlay.get():
            resized_original = cv2.resize(img, (new_w, new_h))
            hsv = cv2.cvtColor(resized_original, cv2.COLOR_BGR2HSV)
            hsv[..., 2] = np.clip(hsv[..., 2] * (brightness.get() / 100), 0, 255).astype(np.uint8)
            adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            stencil_colored = cv2.cvtColor(resized_stencil, cv2.COLOR_GRAY2BGR)
            overlay_img = cv2.addWeighted(adjusted, 0.6, stencil_colored, 0.4, 0)
            show_image(overlay_img)
        else:
            show_image(resized_stencil)

def show_image(array):
    image = Image.fromarray(array)
    imgtk = ImageTk.PhotoImage(image=image)
    image_label.config(image=imgtk)
    image_label.image = imgtk

def save_image():
    if current_image_path:
        img = cv2.imread(current_image_path)
        if img is None:
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, threshold1.get(), threshold2.get())
        kernel = np.ones((spread.get(), spread.get()), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)

        if invert.get():
            dilated = cv2.bitwise_not(dilated)

        height, width = dilated.shape
        new_w = resolution.get()
        new_h = int((new_w / width) * height)
        resized = cv2.resize(dilated, (new_w, new_h), interpolation=cv2.INTER_AREA)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            cv2.imwrite(save_path, resized)

root = Tk()
root.title("Tattoo Stencil Generator")
root.geometry("800x900")  #preferred window size

frame_resolution = Frame(root)
resolution = Scale(frame_resolution, from_=100, to=2000, orient='horizontal', command=update_preview)
resolution.set(800)
resolution.pack()
Label(frame_resolution, text="Resolution Width").pack()
frame_resolution.pack()

frame_spread = Frame(root)
spread = Scale(frame_spread, from_=1, to=10, orient='horizontal', command=update_preview)
spread.set(3)
spread.pack()
Label(frame_spread, text="Spread").pack()
frame_spread.pack()

frame_thresh1 = Frame(root)
threshold1 = Scale(frame_thresh1, from_=0, to=500, orient='horizontal', command=update_preview)
threshold1.set(100)
threshold1.pack()
Label(frame_thresh1, text="Lower Threshold1").pack()
frame_thresh1.pack()

frame_thresh2 = Frame(root)
threshold2 = Scale(frame_thresh2, from_=0, to=500, orient='horizontal', command=update_preview)
threshold2.set(200)
threshold2.pack()
Label(frame_thresh2, text="Upper Threshold2").pack()
frame_thresh2.pack()

invert = IntVar()
Checkbutton(root, text="Invert Colors", variable=invert, command=update_preview).pack()

overlay = IntVar()
Checkbutton(root, text="Overlay Stencil on Original Image", variable=overlay, command=update_preview).pack()

frame_brightness = Frame(root)
brightness = Scale(frame_brightness, from_=10, to=200, orient='horizontal', command=update_preview)
brightness.set(100)
brightness.pack()
Label(frame_brightness, text="Original Image Brightness (%)").pack()
frame_brightness.pack()


Button(root, text="Load Image", command=load_image).pack(pady=10)
Button(root, text="Save Image", command=save_image).pack(pady=5)
image_label = Label(root)
image_label.pack()

root.mainloop()