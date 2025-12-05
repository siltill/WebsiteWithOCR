<template>
  <div id="app-container">
    <header>
      <h1>Сервис Распознавания Текста (OCR)</h1>
      <nav>
        <RouterLink to="/">Главная</RouterLink>
        <RouterLink to="/ocr">Распознать текст</RouterLink>
      </nav>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Добавим немного стилей для красоты */
#app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}
header {
  border-bottom: 1px solid #ddd;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}
header h1 {
  text-align: center;
  color: #42b983;
}
nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
}
nav a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}
nav a.router-link-exact-active {
  color: #42b983;
}
</style>