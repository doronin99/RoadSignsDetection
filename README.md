# Road sign detector
## Описание задачи
### Задача
Создание приложения для распознавания дорожных знаков РФ
### Кем и когда может быть использовано:
- Приложение может быть использовано службами по контролю безопасности дорожного движения для анализа ДТП
- Приложение может быть использовано для помощи слабовидящим водителям
### Ограничения:
- на данном этапе планируется демонстрация работы в качестве веб-сервиса, поэтому невозможна работа в режиме реального времени
- не все знаки могут быть качественно распознаны из-за малой представленности некоторых знаков в обучающих данных
- распознаются только знаки РФ

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
   Выбор 29 классов обусловлен представленностью классов в датасете для обучения модели. Классы, которые представлены слишком малым количеством изображений (< 700) были отфильтрованы

## Эксперименты:

| Модель  | Датасет                                           | Параметры                                                          | Метрики                     |
|---------|---------------------------------------------------|--------------------------------------------------------------------|-----------------------------|
| yolov8s | Russian traffic sign images (20k train,4k valid)  | imgsz=1280, epochs=25, batch=4                                     | mAP50=0.46, mAP50-95=0.35   |
| yolov8s | Traffic Signs Dataset in YOLO format (4 classes)  | imgsz=1280, epochs=25, batch=4                                     | mAP50=0.99, mAP50-95=0.87   |
| yolov8s | Russian traffic sign images (179k,40 top classes) | imgsz=640, epochs=20, batch=64                                     | mAP50=0.66, mAP50-95=0.47   |
| yolov8m | Russian traffic sign images (179k,40 top classes) | imgsz=640, epochs=5, batch=32                                      | mAP50=0.67, mAP50-95=0.49   |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=5, batch=8, optimizer='AdamW'                    | mAP50=0.74, mAP50-95=0.52   |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=20, batch=8, optimizer='AdamW' + albumentations  | mAP50=0.89, mAP50-95=0.65   |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=20, batch=8, optimizer='AdamW' + albumentations  | mAP50=0.92, mAP50-95=0.68   |
| yolov8s | Russian traffic sign images (179k,8 classes)      | imgsz=640, epochs=50, batch=8, optimizer='AdamW' + augmentations   | mAP50=0.922, mAP50-95=0.686 |
| yolov8s | Russian traffic sign images (179k,29 classes)     | imgsz=640, epochs=100, batch=8, optimizer='AdamW' + albumentations | mAP50=0.672, mAP50-95=0.62  |
| yolov8n | Russian traffic sign images (179k,29 classes)     | imgsz=640, epochs=100, batch=8, optimizer='AdamW' + albumentations | mAP50=0.872, mAP50-95=0.614 |

## Трекинг экспериментов:
Для трекинга экспериментов использовался ClearML.

## Аугментации:
SafeRotate, RandomBrightness, Blur, RandomCrop

## Выбор модели:
Выбор модели обуславливался невысокой вычислительной сложностью модели и скоростью инференса модели, так как основные устройства для запуска помошника - портативные устройства (мобильный телефон, видеорегистратор)
Для выбора модели мы протестировали скорость инференса трех моделей с наивысшими метриками для 29 классов.
| Название модели | Скорость инференса (onnx)  одного кадра, мс |
|-----------------|-------------------------------------|
| yolov8s         | 0,77                                |
| yolov8n         | 0,31                                |

В качестве скорости инференса используется среднее значение времени обнаружения знаков на изображении в разрешении 1280х720 на CPU.
Скорость двух моделей позволяет получать предсказания даже на высокой скорости. Наиболее производительное решение - **Yolov8s**

Основная метрика для выбора модели - **mAP50-95** - так как она учитвает точность, пересечение по области (Iou),а диапазон 50-95 обеспечивает высокую точность детекции, что особенно важно при использовании модели в различных погодных и световых условиях.

## Оценка решения:
Решение верно детектирует знаки дорожного движения, скорость работы подходит для реализации приложений на портативных устройствах. Возможно улучшение решения путем увеличения количества эпох обучения и выбора модели большего размера.

## График обучения лучшй модели:
[![results-plot-image.png](https://i.postimg.cc/d1GwGLzT/results-plot-image.png)](https://postimg.cc/JD7fL471)

## Датасеты:

* https://www.kaggle.com/datasets/watchman/rtsd-dataset/data
* https://www.kaggle.com/datasets/valentynsichkar/traffic-signs-dataset-in-yolo-format/data

## Установка зависимостей 
1. `conda env create -n RoadSignDetector -f environment.yml`
2. `conda activte RoadSignDetector`

## Веса моделей
1. загрузите [веса модели](https://drive.google.com/file/d/1Kz4Iwc8lURpjwq1Om_z2NGfODRNX7PsC/view?usp=sharing)
1. положите загруженный файл в директорию `models`

## Запуск

1. `cd server && python main.py`
2. `cd ..\app && python -m streamlit run .\app.py`
3. Сервис доступен по адресу `http://localhost:8501`

## [Демо](https://drive.google.com/file/d/1wNvuS2sbH6FceSxYvt6IGAZ6S48bCynD/view?usp=sharing)

