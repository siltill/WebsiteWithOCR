from pdf2image import convert_from_path
from PIL import Image

def load_image(file_path):
    """
    Загружает файл (изображение или PDF) и возвращает:
    - объект PIL Image для обычного изображения;
    - список объектов PIL Image для многостраничного PDF.
    Всегда конвертирует в 'RGB', чтобы обеспечить единообразие.
    """
    image = None

    try:
        if file_path.lower().endswith('.pdf'):
            # Конвертируем все страницы PDF в изображения
            pages = convert_from_path(file_path)
            if pages:
                # Приводим каждую страницу к формату RGB
                image = [page.convert('RGB') for page in pages]
        else:
            # Открываем файл изображения
            image = Image.open(file_path).convert('RGB')

    except Exception as e:
        # Эта ошибка будет поймана в main.py
        raise ValueError(f"Ошибка при загрузке файла: {e}")

    if image is None:
        raise ValueError("Не удалось обработать файл. Убедитесь, что это изображение или PDF-документ.")
        
    return image
