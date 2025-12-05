# ---------- СТАДИЯ СБОРКИ GO ----------
FROM golang:1.22-bookworm AS builder

WORKDIR /app/backend

# Если у тебя есть go.mod – копируем его
COPY backend/go.mod ./

# (Не обязательно, но можно)
RUN go mod tidy || true

# Копируем остальной код
COPY backend/. .

# Собираем бинарник
RUN go build -o /app/server main.go

# ---------- РАНТАЙМ ----------
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng \
    poppler-utils \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app/backend

COPY --from=builder /app/server ./server
COPY python_core /app/python_core

RUN pip3 install --break-system-packages --no-cache-dir -r /app/python_core/requirements.txt

ENV TESSERACT_PATH=/usr/bin/tesseract
ENV POPPLER_PATH=/usr/bin

EXPOSE 8080
CMD ["./server"]
