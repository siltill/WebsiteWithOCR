package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

// Структура для ответа от Python-скрипта
type OcrResponse struct {
	Text              string  `json:"text"`
	Error             string  `json:"error,omitempty"`
	AverageConfidence float64 `json:"average_confidence"`
	ProcessingTimeMs  int     `json:"processing_time_ms"`
}

// Middleware для CORS
func enableCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*") // В продакшене лучше указать конкретный домен
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Метод не поддерживается", http.StatusMethodNotAllowed)
		return
	}

	// Парсим multipart-форму, 10 MB лимит
	if err := r.ParseMultipartForm(10 << 20); err != nil {
		http.Error(w, "Не удалось разобрать форму", http.StatusBadRequest)
		return
	}

	// Получаем файл из формы
	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Не удалось получить файл из запроса", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Создаем временный файл
	tempFile, err := os.CreateTemp("", "upload-*"+filepath.Ext(handler.Filename))
	if err != nil {
		http.Error(w, "Не удалось создать временный файл", http.StatusInternalServerError)
		return
	}
	defer os.Remove(tempFile.Name()) // Очищаем после завершения
	defer tempFile.Close()

	// Копируем содержимое загруженного файла во временный
	if _, err := io.Copy(tempFile, file); err != nil {
		http.Error(w, "Не удалось сохранить файл", http.StatusInternalServerError)
		return
	}

	// Закрываем файл перед передачей его в другой процесс
	tempFile.Close()

	// Выполняем Python скрипт
	pythonScriptPath := "../python_core/main.py"
	cmd := exec.Command("python", pythonScriptPath, tempFile.Name())

	output, err := cmd.CombinedOutput()
	if err != nil {
		log.Printf("Ошибка выполнения Python скрипта: %v\nВывод: %s", err, string(output))
		http.Error(w, fmt.Sprintf("Ошибка на сервере при обработке файла: %s", string(output)), http.StatusInternalServerError)
		return
	}

	// Декодируем JSON ответ от скрипта
	var ocrResult OcrResponse
	if err := json.Unmarshal(output, &ocrResult); err != nil {
		log.Printf("Ошибка декодирования JSON: %v\nПолученный вывод: %s", err, string(output))
		http.Error(w, "Не удалось декодировать ответ от обработчика", http.StatusInternalServerError)
		return
	}

	// Проверяем, не вернул ли скрипт ошибку внутри JSON
	if ocrResult.Error != "" {
		http.Error(w, "Ошибка при обработке файла: "+ocrResult.Error, http.StatusInternalServerError)
		return
	}

	// Отправляем результат клиенту
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(ocrResult)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/upload", uploadHandler)

	handler := enableCORS(mux)

	port := "8080"
	log.Printf("Сервер запущен на порту %s", port)
	if err := http.ListenAndServe(":"+port, handler); err != nil {
		log.Fatalf("Не удалось запустить сервер: %v", err)
	}
}
