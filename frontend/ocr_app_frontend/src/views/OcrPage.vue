<template>
  <div class="ocr-page">
    <h2>Загрузка файла для распознавания</h2>
    <div class="upload-area">
      <input type="file" @change="handleFileSelect" accept="image/*,application/pdf" ref="fileInput" class="file-input">
      <button @click="triggerFileInput" class="select-button">Выбрать файл</button>
      <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
    </div>

    <button @click="handleUpload" :disabled="!selectedFile || isLoading" class="upload-button">
      {{ isLoading ? 'Обработка...' : 'Загрузить и распознать' }}
    </button>

    <div v-if="error" class="error-message">
      <strong>Ошибка:</strong> {{ error }}
    </div>

    <div v-if="result" class="result-area">
      <h3>Результаты обработки:</h3>
      <div class="metadata">
        <span>Средняя уверенность: <strong>{{ result.average_confidence }}%</strong></span>
        <span>Время обработки: <strong>{{ result.processing_time_ms }} мс</strong></span>
      </div>
      <div class="text-output">
        <p>{{ result.text }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      isLoading: false,
      result: null,
      error: null
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
      this.result = null;
      this.error = null;
    },
    async handleUpload() {
      if (!this.selectedFile) return;

      this.isLoading = true;
      this.error = null;
      this.result = null;

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await axios.post('http://localhost:8080/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.result = response.data;
      } catch (err) {
        this.error = err.response?.data || 'Произошла непредвиденная ошибка. Убедитесь, что бэкенд-сервер запущен.';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.ocr-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.upload-area {
  border: 2px dashed #ccc;
  padding: 2rem;
  text-align: center;
  border-radius: 10px;
}
.file-input {
  display: none;
}
.select-button, .upload-button {
  padding: 10px 20px;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}
.upload-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.file-name {
  margin-left: 1rem;
  font-style: italic;
  color: #555;
}
.error-message {
  color: #d9534f;
  background-color: #f2dede;
  border: 1px solid #d9534f;
  padding: 1rem;
  border-radius: 5px;
}
.result-area {
  margin-top: 1rem;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
.metadata {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
  color: #666;
}
.text-output {
  white-space: pre-wrap; /* Сохраняет пробелы и переносы строк */
  line-height: 1.6;
}
</style>