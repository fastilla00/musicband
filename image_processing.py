import cv2
import numpy as np
from ultralytics import YOLO

# Инициализация YOLO модели
def initialize_yolo(model_path):
    model = YOLO(model_path)
    return model

# Обработка кадра и извлечение параметров руки
def process_frame(frame, model):
    # Конвертация кадра в формат для YOLO
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Запуск модели YOLO для обнаружения
    results = model.predict(source=rgb_frame, conf=0.5, show=False, save=False)

    # Получение данных об объектах (руках)
    detections = results[0].boxes.data.cpu().numpy() if results[0].boxes is not None else []

    hand_data = []
    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection
        if int(class_id) == 0:  # Класс "рука"
            hand_data.append({
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "confidence": float(confidence)
            })

    return hand_data

# Преобразование данных о руках в музыкальные параметры
def map_hand_to_params(hand_data):
    if not hand_data:
        return {
            "pitch": 0,
            "volume": 0,
            "tempo": 0
        }

    # Берём данные первой распознанной руки
    hand = hand_data[0]
    x1, y1, x2, y2 = hand["bbox"]

    # Пример преобразования положения руки в параметры
    bbox_width = x2 - x1
    bbox_height = y2 - y1
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    # Нормализация параметров
    pitch = normalize(center_y, 0, 720, 40, 80)  # Нота (MIDI pitch)
    volume = normalize(bbox_width * bbox_height, 0, 300000, 0.1, 1.0)  # Громкость
    tempo = normalize(center_x, 0, 1280, 60, 180)  # Темп

    return {
        "pitch": int(pitch),
        "volume": round(volume, 2),
        "tempo": int(tempo)
    }

# Утилита для нормализации значений
def normalize(value, min_val, max_val, new_min, new_max):
    value = max(min(value, max_val), min_val)
    return new_min + (value - min_val) * (new_max - new_min) / (max_val - min_val)
