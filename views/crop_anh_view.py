import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime

class CropperWindow(ctk.CTkToplevel):
    def __init__(self, master, image_path, callback):
        super().__init__(master)
        self.title("Crop ảnh")
        self.attributes('-topmost', True)
        self.callback = callback

        self.original_image = Image.open(image_path)

        max_width, max_height = 800, 600
        self.scale_x = self.scale_y = 1
        self.display_image = self.original_image.copy()

        if self.original_image.width > max_width or self.original_image.height > max_height:
            self.display_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            self.scale_x = self.original_image.width / self.display_image.width
            self.scale_y = self.original_image.height / self.display_image.height

        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas = ctk.CTkCanvas(self, width=self.tk_image.width(), height=self.tk_image.height(), cursor="cross")
        self.canvas.pack(padx=10, pady=10)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        margin = 50
        self.rect_start_x = margin
        self.rect_start_y = margin
        self.rect_end_x = self.tk_image.width() - margin
        self.rect_end_y = self.tk_image.height() - margin

        self.rect = self.canvas.create_rectangle(
            self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y,
            outline="red", width=2
        )

        self.overlay_ids = []
        self.corner_lines = []
        self.update_overlay()
        self.update_corner_lines()

        self.dragging = None
        self.start_drag_x = self.start_drag_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.save_button = ctk.CTkButton(self, text="Cắt và lưu", command=self.crop_and_save)
        self.save_button.pack(pady=12)

    def update_overlay(self):
        # Xoá overlay cũ
        for oid in self.overlay_ids:
            self.canvas.delete(oid)
        self.overlay_ids.clear()

        x1, y1, x2, y2 = self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y
        width = self.tk_image.width()
        height = self.tk_image.height()

        # Tạo 4 vùng che mờ bên ngoài khung crop
        self.overlay_ids.append(self.canvas.create_rectangle(0, 0, width, y1, fill='black', stipple='gray50'))
        self.overlay_ids.append(self.canvas.create_rectangle(0, y2, width, height, fill='black', stipple='gray50'))
        self.overlay_ids.append(self.canvas.create_rectangle(0, y1, x1, y2, fill='black', stipple='gray50'))
        self.overlay_ids.append(self.canvas.create_rectangle(x2, y1, width, y2, fill='black', stipple='gray50'))

    def update_corner_lines(self):
        for line in self.corner_lines:
            self.canvas.delete(line)
        self.corner_lines.clear()

        x1, y1, x2, y2 = self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y
        length = 15
        color = "red"
        width = 2

        # Góc trái trên
        self.corner_lines.append(self.canvas.create_line(x1, y1, x1 + length, y1, fill=color, width=width))
        self.corner_lines.append(self.canvas.create_line(x1, y1, x1, y1 + length, fill=color, width=width))

        # Góc phải trên
        self.corner_lines.append(self.canvas.create_line(x2, y1, x2 - length, y1, fill=color, width=width))
        self.corner_lines.append(self.canvas.create_line(x2, y1, x2, y1 + length, fill=color, width=width))

        # Góc trái dưới
        self.corner_lines.append(self.canvas.create_line(x1, y2, x1 + length, y2, fill=color, width=width))
        self.corner_lines.append(self.canvas.create_line(x1, y2, x1, y2 - length, fill=color, width=width))

        # Góc phải dưới
        self.corner_lines.append(self.canvas.create_line(x2, y2, x2 - length, y2, fill=color, width=width))
        self.corner_lines.append(self.canvas.create_line(x2, y2, x2, y2 - length, fill=color, width=width))

    def get_crop_coords(self):
        return (
            int(self.rect_start_x * self.scale_x),
            int(self.rect_start_y * self.scale_y),
            int(self.rect_end_x * self.scale_x),
            int(self.rect_end_y * self.scale_y)
        )

    def crop_and_save(self):
        coords = self.get_crop_coords()
        cropped = self.original_image.crop(coords)
        save_dir = os.path.join("resources", "images_history")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"cropped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        temp_path = os.path.join(save_dir, filename)
        cropped.save(temp_path)
        self.attributes('-topmost', False)
        self.callback(temp_path)
        self.destroy()

    def detect_drag_area(self, x, y):
        margin = 10
        x1, y1, x2, y2 = self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y

        if abs(x - x1) <= margin and abs(y - y1) <= margin:
            return 'top_left'
        if abs(x - x2) <= margin and abs(y - y1) <= margin:
            return 'top_right'
        if abs(x - x1) <= margin and abs(y - y2) <= margin:
            return 'bottom_left'
        if abs(x - x2) <= margin and abs(y - y2) <= margin:
            return 'bottom_right'

        if abs(x - x1) <= margin and y1 + margin < y < y2 - margin:
            return 'left'
        if abs(x - x2) <= margin and y1 + margin < y < y2 - margin:
            return 'right'
        if abs(y - y1) <= margin and x1 + margin < x < x2 - margin:
            return 'top'
        if abs(y - y2) <= margin and x1 + margin < x < x2 - margin:
            return 'bottom'

        if x1 < x < x2 and y1 < y < y2:
            return 'move'

        return None

    def on_mouse_down(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.dragging = self.detect_drag_area(x, y)
        self.start_drag_x = x
        self.start_drag_y = y

    def on_mouse_drag(self, event):
        if not self.dragging:
            return

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        dx = x - self.start_drag_x
        dy = y - self.start_drag_y

        if self.dragging == 'move':
            self.rect_start_x += dx
            self.rect_end_x += dx
            self.rect_start_y += dy
            self.rect_end_y += dy
        elif self.dragging == 'left':
            self.rect_start_x += dx
        elif self.dragging == 'right':
            self.rect_end_x += dx
        elif self.dragging == 'top':
            self.rect_start_y += dy
        elif self.dragging == 'bottom':
            self.rect_end_y += dy
        elif self.dragging == 'top_left':
            self.rect_start_x += dx
            self.rect_start_y += dy
        elif self.dragging == 'top_right':
            self.rect_end_x += dx
            self.rect_start_y += dy
        elif self.dragging == 'bottom_left':
            self.rect_start_x += dx
            self.rect_end_y += dy
        elif self.dragging == 'bottom_right':
            self.rect_end_x += dx
            self.rect_end_y += dy

        self.rect_start_x = max(0, min(self.rect_start_x, self.tk_image.width()))
        self.rect_end_x = max(0, min(self.rect_end_x, self.tk_image.width()))
        self.rect_start_y = max(0, min(self.rect_start_y, self.tk_image.height()))
        self.rect_end_y = max(0, min(self.rect_end_y, self.tk_image.height()))

        self.start_drag_x = x
        self.start_drag_y = y

        self.canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y)
        self.update_overlay()
        self.update_corner_lines()

    def on_mouse_up(self, event):
        self.dragging = None
