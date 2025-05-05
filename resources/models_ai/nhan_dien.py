import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class DigitRecognizer:
    def __init__(self, model_path=r"resources\models_ai\mnist_cnn_finetuned.h5"):
        self.model = tf.keras.models.load_model(model_path)

    def preprocess_digit(self, roi):
        input_tensor = np.expand_dims(roi, axis=(0, -1))  # shape (1, 28, 28, 1)
        return input_tensor

    def recognize(self, image, visualize=True):
        height, width = image.shape[:2]
        top, bottom, left, right = 7, 7, 3, 3
        cropped_image = image[top:height - bottom, left:width - right]

        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        vertical_sum = np.sum(thresh, axis=0)
        threshold = np.max(vertical_sum) * 0.05
        in_digit = False
        digit_regions = []
        start = 0

        for i, val in enumerate(vertical_sum):
            if val > threshold and not in_digit:
                start = i
                in_digit = True
            elif val <= threshold and in_digit:
                end = i
                in_digit = False
                if end - start > 3:
                    digit_regions.append((start, end))
        if in_digit:
            digit_regions.append((start, len(vertical_sum) - 1))

        result = ""
        output = cropped_image.copy()
        region_heights = []
        processed_regions = []

        for start, end in digit_regions:
            digit_roi = thresh[:, start:end]
            ys = np.any(digit_roi, axis=1)
            if not np.any(ys):
                continue
            y1, y2 = np.where(ys)[0][[0, -1]]
            height = y2 - y1
            region_heights.append(height)
            processed_regions.append((start, end, y1, y2, digit_roi))

        if not region_heights:
            print("⚠️ Không tìm thấy vùng số.")
            return ""

        avg_height = np.mean(region_heights)

        for start, end, y1, y2, digit_roi in processed_regions:
            h = y2 - y1
            is_dot = h < avg_height / 2

            if is_dot:
                label = "."
            else:
                digit_roi = digit_roi[y1:y2 + 1, :]
                digit_roi = cv2.copyMakeBorder(digit_roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
                digit_roi = cv2.resize(digit_roi, (28, 28), interpolation=cv2.INTER_AREA)
                input_tensor = self.preprocess_digit(digit_roi)
                pred = self.model.predict(input_tensor, verbose=0)[0]
                label = str(np.argmax(pred))

            result += label

            if visualize:
                color = (255, 0, 0) if is_dot else (0, 255, 0)
                cv2.rectangle(output, (start, y1), (end, y2), color, 1)
                cv2.putText(output, label, (start, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        print("👉 Dự đoán:", result)

        # if visualize:
        #     plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        #     plt.title("Tách và nhận diện từng số trong ô")
        #     plt.axis("off")
        #     plt.show()

        return result
