# ---------- СБОРКА VUE (Vite) ----------
FROM node:20-alpine AS builder

WORKDIR /app

# Сначала package*.json из правильной папки
COPY frontend/ocr_app_frontend/package*.json ./
RUN npm install

# Затем весь фронт
COPY frontend/ocr_app_frontend/. .

# Прод-сборка
RUN npm run build

# ---------- NGINX ДЛЯ ОТДАЧИ СТАТИКИ ----------
FROM nginx:alpine

# Удаляем дефолтный конфиг и добавляем наш
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Копируем собранный фронт
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
