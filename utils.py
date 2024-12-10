import math

def normalize(value, min_val, max_val, new_min, new_max):
    """
    Нормализует значение из одного диапазона в другой.

    :param value: Значение для нормализации.
    :param min_val: Минимум исходного диапазона.
    :param max_val: Максимум исходного диапазона.
    :param new_min: Минимум целевого диапазона.
    :param new_max: Максимум целевого диапазона.
    :return: Нормализованное значение.
    """
    if max_val - min_val == 0:
        return new_min
    return new_min + (new_max - new_min) * (value - min_val) / (max_val - min_val)

def clamp(value, min_val, max_val):
    """
    Ограничивает значение заданными пределами.

    :param value: Значение для ограничения.
    :param min_val: Нижний предел.
    :param max_val: Верхний предел.
    :return: Ограниченное значение.
    """
    return max(min_val, min(value, max_val))

def get_hand_angle(coords):
    """
    Вычисляет угол наклона руки по координатам.

    :param coords: Список координат (x, y) для ключевых точек руки.
    :return: Угол наклона в градусах.
    """
    if len(coords) < 2:
        return 0

    x1, y1 = coords[0]
    x2, y2 = coords[1]

    delta_x = x2 - x1
    delta_y = y2 - y1

    angle = math.degrees(math.atan2(delta_y, delta_x))
    return angle

def distance_between_points(p1, p2):
    """
    Вычисляет расстояние между двумя точками.

    :param p1: Первая точка (x, y).
    :param p2: Вторая точка (x, y).
    :return: Расстояние между точками.
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def is_fist_closed(hand_landmarks):
    """
    Определяет, сжата ли рука в кулак на основе расстояния между ключевыми точками.

    :param hand_landmarks: Словарь или структура с координатами ключевых точек руки.
    :return: True, если рука сжата в кулак, иначе False.
    """
    # Пример: сравнение расстояний между кончиками пальцев и основанием ладони
    try:
        thumb_tip = hand_landmarks['thumb_tip']
        index_base = hand_landmarks['index_base']
        thumb_base = hand_landmarks['thumb_base']

        distance_thumb = distance_between_points(thumb_tip, thumb_base)
        distance_index = distance_between_points(index_base, thumb_base)

        # Простая эвристика: если большой палец и основание находятся близко,
        # возможно, рука сжата в кулак.
        return distance_thumb < distance_index * 0.5
    except KeyError:
        return False

def smooth_value(value, previous_value, smoothing_factor=0.5):
    """
    Плавно изменяет значение, чтобы уменьшить резкие скачки.

    :param value: Текущее значение.
    :param previous_value: Предыдущее значение.
    :param smoothing_factor: Коэффициент сглаживания (0.0 - нет сглаживания, 1.0 - полное игнорирование текущего значения).
    :return: Сглаженное значение.
    """
    return previous_value * smoothing_factor + value * (1 - smoothing_factor)
