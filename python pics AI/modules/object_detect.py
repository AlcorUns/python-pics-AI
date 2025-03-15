from ultralytics import YOLO
import cv2
import os
import numpy as np

def detect_object(img_path):
    try:
        model = YOLO('yolov8n.pt')   #Интерпретация предобученной модели обнаружения объектов
        img = cv2.imread(img_path)   #Чтение изображения
        results = model(img)[0]       #Детекция изображения
        class_names = results.names
        classes = results.boxes.cls.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
        confidences = results.boxes.conf.cpu().numpy()

        def print_box(class_name, coords, conf):  #Функция вывода данных
            print(f"Тип объекта: {class_name}")
            print(f"Координаты: {coords}")
            print(f"Вероятность: {conf:.2f}")
            print("---")

        grouped_data={}
        
        if results:
            for class_id, box, conf in zip(classes, boxes, confidences):           #сбор данных и помещение в заготовленный список
                class_name = class_names[int(class_id)]         #Перебор типов объектов по id
                conf = round(float(conf), 2)
                x1, y1, x2, y2 = box
                if class_name not in grouped_data:
                        grouped_data[class_name]=[]
                grouped_data[class_name].append((box, conf)) #Добавление данных в список

                print_box(class_name, [x1, y1, x2, y2], conf)  #Вывод полученных данных в консоль

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  #Рисование рамки объекта и создание подписи
                cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            new_img_path = os.path.splitext(img_path)[0] + '_yolo' + os.path.splitext(img_path)[1]  #Сохранение обработанного изображения
            cv2.imwrite(new_img_path, img)

            meta_path = os.path.splitext(img_path)[0] + '_data.txt'  #Создание файла с мета-данными
            with open(meta_path, 'w', encoding='utf-8') as f:
                for class_name, details in grouped_data.items():
                    f.write(f"\nТип объекта: {class_name}\n")
                    for detail, conf in details:
                        f.write(f"Координаты: ({detail[0]}, {detail[1]}, {detail[2]}, {detail[3]})\n")
                        f.write(f"Вероятность: {conf:.2f}\n")
            print(f"Обработанное изображение сохранено в {new_img_path}")
            print(f"Мета-данные сохранены в {meta_path}\n\n")
        else:
            print("\nОбъекты не найдены.\n")
            
    except FileNotFoundError:
        print("Изображение не найдено")
    
# detect_object("C:/Users/Admin/Desktop/python pics AI/img.jpg")