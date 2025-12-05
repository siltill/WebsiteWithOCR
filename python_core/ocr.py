import pytesseract
from pytesseract import Output

def get_text_from_image(processed_image):
    """
    Извлекает текст и данные об уверенности из обработанного изображения.
    Принимает CV2 Image (numpy array).
    """
    
    # --psm 6, работает стабильнее, чем 3
    custom_config = r'-l rus --oem 3 --psm 6'
    
    # Используем image_to_data для получения детальной информации
    data = pytesseract.image_to_data(processed_image, config=custom_config, output_type=Output.DICT)
    
    full_text = []
    confidences = []
    
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > -1:
            word = data['text'][i]
            if word.strip():
                full_text.append(word)
                confidences.append(float(data['conf'][i]))
    
    return " ".join(full_text), confidences
