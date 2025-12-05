<template>
  <div class="home-page">
    <h2>Добро пожаловать!</h2>
    <p>
      Это простой веб-инструмент для извлечения текста из изображений и PDF-файлов.
      Наш сервис использует современные технологии машинного обучения для обеспечения
      высокой точности распознавания русского текста.
    </p>
    <p>
      Чтобы начать, перейдите на страницу распознавания и загрузите ваш файл.
    </p>
    <RouterLink to="/ocr" class="start-button">Начать работу</RouterLink>
  </div>
</template>

<style scoped>
.home-page {
  text-align: center;
}
.start-button {
  display: inline-block;
  margin-top: 1.5rem;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 1.1rem;
}
</style>