# 1. Stage: base system + Ollama
FROM ubuntu:22.04 AS ollama

# Zmienne środowiskowe dla bezinteraktywnej instalacji
ENV DEBIAN_FRONTEND=noninteractive

# Zainstaluj niezbędne narzędzia
RUN apt-get update && \
    apt-get install -y curl gnupg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Dodaj klucz i repozytorium Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# (opcjonalnie) Pre-pull model Llama 3, aby był dostępny od razu w obrazie
RUN ollama pull llama3

# 2. Stage: aplikacja FastAPI
FROM python:3.10-slim

# Przekopiuj instalację Ollama z poprzedniego etapu
COPY --from=ollama /usr/local/bin/ollama /usr/local/bin/ollama
COPY --from=ollama /usr/local/share/ollama /usr/local/share/ollama

# Pracuj w katalogu /app
WORKDIR /app

# Zainstaluj zależności Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY . .

# Exponuj port (domyślnie FastAPI na 8000)
EXPOSE 8000

# Domyślny entrypoint: uruchom Ollama (opcjonalnie) i FastAPI
CMD ["sh", "-c", "\
    # Upewnij się, że Ollama działa w tle (daemon) \
    ollama serve & \
    # Uruchom FastAPI przez uvicorn \
    exec uvicorn main:app --host 0.0.0.0 --port 8000\
"]
