import cv2
import numpy as np

def deskew(binary_image):
    try:
        coords = np.column_stack(np.where(binary_image > 0))
        angle = cv2.minAreaRect(coords)[-1] 

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = binary_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        rotated = cv2.warpAffine(binary_image, M, (w, h), 
                                 flags=cv2.INTER_CUBIC, 
                                 borderMode=cv2.BORDER_CONSTANT, 
                                 borderValue=0)
        
        return rotated
    
    except Exception as e:
        return binary_image

def preprocess_image(image):
    """
    Выполняет полную предобработку изображения для OCR.
    """
    # 1. Конвертация из PIL в CV2 (OpenCV)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 2. Конвертация в оттенки серого
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # 3. Масштабирование
    h, w = gray.shape
    if w < 1000:
        scale = 1.5
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

    # 4. Удаление шума
    # denoised = cv2.medianBlur(gray, 3)
    denoised = gray # Пропускаем шаг

    # 5. Бинаризация (Порог Оцу)
    _, binary_image = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 6. Выравнивание
    # deskewed_image = deskew(binary_image)
    deskewed_image = binary_image # Пропускаем шаг
    
    return deskewed_image
