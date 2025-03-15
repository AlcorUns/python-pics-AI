import easyocr

def detect_text(img_path):
    try:                                         
        reader = easyocr.Reader(["ru"], verbose=False)
        result = reader.readtext(img_path, paragraph=True)
        if result:                                              
            extracted_text = "\n".join([text[1] for text in result])
            return extracted_text
        else:
            print("Текст не найден")
    except FileNotFoundError:
        print("Изображение не найдено")
    
# print(detect_text("C:/Users/Admin/Desktop/python pics AI/img.jpg"))