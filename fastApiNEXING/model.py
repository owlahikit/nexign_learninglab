# импорт библиотеки os
import os
# импорт библиотеки ultralytics
from ultralytics import YOLO

# сборка модели
model = YOLO('yolov8m-seg.yaml')  # сборка модели из официального YAML-файла
model = YOLO('yolov8m-seg.pt')  # загрузка предобученной модели (рекомендовано)
model = YOLO('yolov8m-seg.yaml').load('yolov8m-seg.pt')  # создает экземпляр модели YOLO с заданной конфигурацией

# обращение к весам модели
model = YOLO('yolov8m-seg.pt')  # предобученные веса
model = YOLO('C:\\Users\\dimas\\PycharmProjects\\fastApiNEXING\\best.pt')  # кастомные веса после дообучения YOLO


def par(results):
    import numpy as np

    def calculate_polygon_area(points):
        x = points[:, 0]
        y = points[:, 1]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    cls_tensor = results[0].boxes.cls
    if cls_tensor.is_cuda:
        cls_tensor = cls_tensor.cpu()
    cls_tensor = cls_tensor.numpy()
    class_names = ['Другое', 'Мегафон', 'Йота']
    classes = [class_names[int(c)] for c in cls_tensor]

    iota = 0
    megaphone = 0
    other = 0
    points = 0

    masks = results[0].masks.xy
    for mask_i in range(len(masks)):
        if classes[mask_i] == 'Другое':
            other += calculate_polygon_area(np.array(masks[mask_i]))
        elif classes[mask_i] == "Мегафон":
            megaphone += calculate_polygon_area(np.array(masks[mask_i]))
        else:
            iota += calculate_polygon_area(np.array(masks[mask_i]))
    if iota > other and abs(iota - other) > 50:
        points += 2
    if iota < other and abs(iota - other) > 50:
        ...
    if iota == other or abs(iota - other) < 50:
        points += 1
    if megaphone > other and abs(iota - other) > 50:
        points += 2
    if megaphone < other and abs(iota - other) > 50:
        ...
    if megaphone == other or abs(iota - other) < 50:
        points += 1
    return points


def res(link):
    results = model(link)
    if results:
        return par(results)
    else:
        return "No objects detected."
