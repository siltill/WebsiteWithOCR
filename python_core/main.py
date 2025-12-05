import sys
import time
import json

# Импортируем наши модули
from loader import load_image
from preprocessing import preprocess_image
from ocr import get_text_from_image


# Модуль 4: Экспорт данных
def export_data(text, confidence_list, start_time):
    """Формирует и выводит итоговый JSON."""
    end_time = time.time()
    processing_time = int((end_time - start_time) * 1000)  # в миллисекундах

    valid_confidences = [conf for conf in confidence_list if conf > 0]
    average_confidence = (
        sum(valid_confidences) / len(valid_confidences)
        if valid_confidences else 0
    )

    result = {
        "text": text,
        "average_confidence": round(average_confidence, 2),
        "processing_time_ms": processing_time
    }
    
    # ensure_ascii=True, чтобы избежать проблем с кодировкой в Go
    print(json.dumps(result, ensure_ascii=True))


def main(file_path):
    """Главная функция, координирующая весь процесс."""
    start_time = time.time()
    try:
        # Модуль 1: Загрузка
        images = load_image(file_path)

        # Приводим к списку: для PDF это уже список, для обычного изображения — одиночный элемент
        if isinstance(images, list):
            image_list = images
        else:
            image_list = [images]

        all_text_parts = []
        all_confidences = []

        # Обрабатываем каждую страницу/изображение одинаково
        for img in image_list:
            # Модуль 2: Предобработка
            processed_image = preprocess_image(img)

            # Модуль 3: Распознавание
            text, confidences = get_text_from_image(processed_image)

            if text.strip():
                all_text_parts.append(text)

            all_confidences.extend(confidences)

        # Объединяем текст со всех страниц в одну строку
        full_text = "\n\n".join(all_text_parts)

        # Модуль 4: Экспорт
        export_data(full_text, all_confidences, start_time)

    except Exception as e:
        # В случае ошибки возвращаем JSON с ошибкой
        error_result = {
            "error": str(e)
        }
        print(json.dumps(error_result, ensure_ascii=True))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        # Ошибка, если путь к файлу не передан
        error_info = {"error": "Путь к файлу не был передан в скрипт."}
        print(json.dumps(error_info, ensure_ascii=True))
        sys.exit(1)
