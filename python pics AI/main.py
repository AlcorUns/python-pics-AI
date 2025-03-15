from pyaspeller import YandexSpeller
import os
from modules.text_detect import detect_text
from modules.object_detect import detect_object
from flask import Flask

speller = YandexSpeller()    #Подлючение модуля, исправляющего текст

print("Примечания к работе программы:\n"
"1) Если изображение находится внутри проекта, указывайте ссылку в формате \"имя_файла.формат\"\n"
"2) Если изображение находится вне проекта, путь к нему указывайте в формате \"C:/Users/.../имя_файла.формат\"\n"
"3) Чтобы завершить работу программы, вместо пути к файлу укажите стоп-слово \"Завершение\"\n"
"4) Приятного использования!\n")


img_path = input("Введите путь к файлу: ")

while img_path not in ["Завершение", "завершение"]: 
    print("\nI. Обнаружение объектов на фото\n")
    detect_object(img_path)         #Вызов функции обнаружения объектов на фото, вывода данных и их внесения в текстовый файл

    print("II. Обнаружение текста на фото и его исправление\n")
    text = detect_text(img_path)            #Вызов функции обнаружения текста
    fixed_text = speller.spelled(text)      #Вызов функции исправления текста

    print("Текст до исправления:\n", text, "\n---\n"
    "Текст после исправления:\n", fixed_text, "\n\n")

    text_path = os.path.splitext(img_path)[0] + '_text.txt'  #Создание файла с текстом изображения
    with open(text_path, 'w', encoding='utf-8') as f:       #Внесение исправленного и неисправленного текста в текстовый файл
        f.write(f"Текст до исправления: {text}\n")
        f.write(f"Текст после исправления: {fixed_text}\n")
    print(f"Текст сохранен в {text_path}\n.\n.\n.\n")


    img_path = input("Введите путь к файлу: ")