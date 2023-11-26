# Road sign detector
## Ход работы:
1. Выбор датасета - https://www.kaggle.com/datasets/watchman/rtsd-dataset/data
2. Конвертация аннотаций COCO в аннотации YOLO.
3. Анализ датасета.
4. Отбор классов, достаточно представленных в датасете.
5. Проведение экспериментов.
6. Обучение модели.
7. Создание приложения для получения предсказаний модели на видео.

Было обученно две модели: 
1. 8 классов по типам дорожных знаков - [Демонстрация](https://drive.google.com/file/d/18FAGUMIgEBnvvCulXudQmK7Wq9uU_twI/view?usp=drive_link)
2. 29 классов для детекции 29 различных дорожных знаков - [Демонстрация](https://drive.google.com/file/d/12SndJXBaDCoJYB-sJqZxPP2ucQKplaSJ/view?usp=drive_link)

## Эксперименты:

| Модель  | Датасет                                           | Параметры                                                         | Метрики                   |
|---------|---------------------------------------------------|-------------------------------------------------------------------|---------------------------|
| yolov8s | Russian traffic sign images (20k train,4k valid)  | imgsz=1280, epochs=25, batch=4                                    | mAP50=0.46, mAP50-95=0.35 |
| yolov8s | Traffic Signs Dataset in YOLO format (4 classes)  | imgsz=1280, epochs=25, batch=4                                    | mAP50=0.99, mAP50-95=0.87 |
| yolov8s | Russian traffic sign images (179k,40 top classes) | imgsz=640, epochs=20, batch=64                                    | mAP50=0.66, mAP50-95=0.47 |
| yolov8m | Russian traffic sign images (179k,40 top classes) | imgsz=640, epochs=5, batch=32                                     | mAP50=0.67, mAP50-95=0.49 |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=5, batch=8, optimizer='AdamW'                   | mAP50=0.74, mAP50-95=0.52 |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=20, batch=8, optimizer='AdamW' + albumentations | mAP50=0.89, mAP50-95=0.65 |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=20, batch=8, optimizer='AdamW' + albumentations | mAP50=0.92, mAP50-95=0.68 |

## Датасеты:

* https://www.kaggle.com/datasets/watchman/rtsd-dataset/data
* https://www.kaggle.com/datasets/valentynsichkar/traffic-signs-dataset-in-yolo-format/data

## Запуск

1. `cd server && python main.py`
2. `cd ../app && python -m streamlit run .\app.py`
3. Сервис доступен по адресу `http://localhost:8501`
