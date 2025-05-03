import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
from resources.models_ai.nhan_dien import DigitRecognizer

class ImageProcessor:
    def __init__(self, image, recognizer: DigitRecognizer):
        self.image = image
        self.recognizer = recognizer
        self.result_kq = []

    def preprocess(self, img, factor: int):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = Image.fromarray(img)
        enhancer = ImageEnhance.Sharpness(img).enhance(factor)
        if gray.std() < 30:
            enhancer = ImageEnhance.Contrast(enhancer).enhance(factor)
        return np.array(enhancer)

    def postprocess_score(self, score_str):
        try:
            score = float(score_str)
            if 10 < score <= 100:
                score /= 10
            elif score > 100:
                score /= 100
            return round(score, 2)
        except ValueError:
            return score_str

    def extract_and_recognize(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 15, -10)

        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)

        grid = cv2.add(horizontal_lines, vertical_lines)
        contours, _ = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boxes = [cv2.boundingRect(c) for c in contours]
        cells = [box for box in boxes if 40 < box[2] < 500 and 20 < box[3] < 100]
        cells = sorted(cells, key=lambda b: (b[1], b[0]))

        rows, current_row, prev_y = [], [], -100
        for box in cells:
            x, y, w, h = box
            if abs(y - prev_y) > 15 and current_row:
                rows.append(current_row)
                current_row = []
            current_row.append(box)
            prev_y = y
        if current_row:
            rows.append(current_row)

        valid_rows = [row for row in rows if 3 <= len(row) <= 4]

        for idx, row in enumerate(valid_rows):
            row = sorted(row, key=lambda b: b[0])
            mssv_box, diem_box = row[0], row[-1]
            x1, y1, w1, h1 = mssv_box
            x2, y2, w2, h2 = diem_box

            mssv_crop = self.preprocess(self.image[y1:y1+h1, x1:x1+w1], factor=2)
            diem_crop = self.preprocess(self.image[y2:y2+h2, x2:x2+w2], factor=2)

            print(f"\n--- Hàng {idx} ---")
            mssv_kq = self.recognizer.recognize(mssv_crop)
            diem_kq_raw = self.recognizer.recognize(diem_crop)
            diem_kq = self.postprocess_score(diem_kq_raw)

            self.result_kq.append((mssv_kq, diem_kq))

            # plt.figure(figsize=(6, 2))
            # plt.subplot(1, 2, 1)
            # plt.imshow(cv2.cvtColor(mssv_crop, cv2.COLOR_BGR2RGB))
            # plt.title(f"MSSV: {mssv_kq}")
            # plt.axis("off")
            #
            # plt.subplot(1, 2, 2)
            # plt.imshow(cv2.cvtColor(diem_crop, cv2.COLOR_BGR2RGB))
            # plt.title(f"ĐIỂM: {diem_kq}")
            # plt.axis("off")
            # plt.show()

        print("\n📋 Tổng hợp kết quả:")
        for idx, (mssv, diem) in enumerate(self.result_kq, start=1):
            print(f"Hàng {idx}: MSSV = {mssv} | ĐIỂM = {diem}")
