SHELL := /usr/bin/env bash
#ну типа версии и тд да
PYTHON       ?= python
BACKEND_DIR  ?= backend
FRONTEND_DIR ?= frontend
UVICORN_APP  ?= app.main:app   # backend/app/main.py -> app.main:app
HOST         ?= 0.0.0.0
PORT         ?= 8000
#Ну по умолчанию типа если запустить просто make без аргументов, выполнится цель help
.DEFAULT_GOAL := help
#
.PHONY: help \
        backend-dev backend-run backend-test backend-lint backend-format backend-migrate backend-revision \
        frontend-dev frontend-build frontend-test frontend-install \
        docker_up docker_down docker_logs test_docker \
        install clean

#Хелпа
help:
	@echo "Доступные команды:"
	@echo "  make backend-dev       - FastAPI dev сервер (uvicorn --reload)"
	@echo "  make backend-run       - FastAPI сервер без reload"
	@echo "  make backend-test      - pytest бекенда"
    @echo "  make backend-lint      - линтеры бекенда (mypy + ruff)"
    @echo "  make backend-format    - форматирование бекенда (ruff fix + ruff format)"
	@echo "  make backend-migrate   - Alembic upgrade head"
	@echo "  make backend-revision  - Alembic revision --autogenerate"
	@echo "  make frontend-dev      - фронт dev сервер (npm run dev)"
	@echo "  make frontend-build    - сборка фронта (npm run build)"
	@echo "  make frontend-test     - тесты фронта (npm test / npm run test)"
	@echo "  make frontend-install  - npm install во фронте"
	@echo "  make install           - зависимости backend + frontend"
	@echo "  make clean             - очистка __pycache__ и *.pyc"

#Бэкенд
backend-dev:
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn $(UVICORN_APP) --host $(HOST) --port $(PORT) --reload
backend-run:
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn $(UVICORN_APP) --host $(HOST) --port $(PORT)
backend-test:
	cd $(BACKEND_DIR) && pytest
backend-lint:
	cd $(BACKEND_DIR) && mypy .
	cd $(BACKEND_DIR) && ruff check .
backend-format:
	cd $(BACKEND_DIR) && ruff check . --fix
	cd $(BACKEND_DIR) && ruff format .
backend-revision:
	cd $(BACKEND_DIR) && alembic revision --autogenerate -m "auto"
backend-migrate:
	cd $(BACKEND_DIR) && alembic upgrade head

#Фронтенд
frontend-dev:    #Запускает dev‑сервер фронта например, Vite/Next/React‑scripts через npm run dev.
	cd $(FRONTEND_DIR) && npm run dev
frontend-build:  #Собирает production‑бандл фронтенда (npm run build).
	cd $(FRONTEND_DIR) && npm run build
frontend-test:
	cd $(FRONTEND_DIR) && npm test || npm run test
frontend-install:
	cd $(FRONTEND_DIR) && npm install


#Общие приколюхи
install: #Обновляет пип и юзается для того что бы че то скачать
	cd $(BACKEND_DIR) && $(PYTHON) -m pip install --upgrade pip && $(PYTHON) -m pip install -r requirements.txt
	cd $(FRONTEND_DIR) && npm install
clean: #Чистит мусор и может пофиксить
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
