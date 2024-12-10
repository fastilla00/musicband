import cv2
import pygame
from image_processing import initialize_yolo, process_frame, map_hand_to_params
from music_generator import initialize_music, generate_music, stop_music
from visualization import initialize_visualization, update_visualization, stop_visualization
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

def main():
    # 1. Инициализация камеры
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # 2. Инициализация YOLO модели
    print("Загрузка модели YOLO...")
    model = initialize_yolo("models/yolov8-hand.pt")

    # 3. Инициализация музыки
    print("Инициализация музыкального модуля...")
    initialize_music()

    # 4. Инициализация визуализации
    print("Инициализация визуализации...")
    initialize_visualization()

    print("Приложение запущено. Нажмите 'q' для выхода.")

    try:
        while True:
            # 5. Захват кадра с камеры
            ret, frame = camera.read()
            if not ret:
                print("Не удалось получить кадр с камеры.")
                break

            # 6. Обработка кадра и получение параметров руки
            hand_data = process_frame(frame, model)
            music_params = map_hand_to_params(hand_data)

            # 7. Генерация музыки на основе параметров
            generate_music(music_params)

            # 8. Обновление визуализации
            update_visualization(music_params)

            # 9. Отображение видеопотока (опционально для отладки)
            cv2.imshow("Камера", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Остановка приложения.")

    finally:
        # Завершение работы
        camera.release()
        cv2.destroyAllWindows()
        stop_music()
        stop_visualization()
        print("Приложение завершило работу.")

if __name__ == "__main__":
    main()
