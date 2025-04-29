import os
import numpy as np
from PIL import Image
import onnxruntime as ort
"""
Module xử lý dự đoán MSSV và điểm cuối kỳ từ ảnh, dùng model ONNX.
"""
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'cnn_model.onnx')
# Load ONNX model nếu có
session = None
if os.path.isfile(MODEL_PATH):
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
def predict_image(img_path):
    """
    Trả về tuple (mssv: str, diem_ck: float).
    Nếu model chưa có, trả mặc định ('1234567', 9.0).
    """
    if session is None:
        return '1234567', 9.0
    img = Image.open(img_path).convert('RGB').resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))[None, ...]  # CHW format
    pred = session.run([output_name], {input_name: arr})[0][0]
    return str(int(pred[0])), float(pred[1])