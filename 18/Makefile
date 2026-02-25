.PHONY: help dev.install db.migration.new db.migrate db.rollback db.up db.down db.logs

# Цвета для вывода
CYAN := \033[0;36m
RESET := \033[0m

# Переменные окружения
include .env
export

# DATABASE_URL будет формироваться из .env переменных
DATABASE_URL := postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)

help: ## Показать справку по командам
	@echo "$(CYAN)Доступные команды:$(RESET)"
	@grep -E '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'

dev.install: ## Установить зависимости для разработки
	@echo "$(CYAN)Создание виртуального окружения...$(RESET)"
	python3 -m venv venv
	@echo "$(CYAN)Установка зависимостей...$(RESET)"
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "$(CYAN)✓ Зависимости установлены$(RESET)"

db.migration.new: ## Создать новую миграцию (использование: make db.migration.new name="описание")
ifndef name
	$(error Укажите имя миграции: make db.migration.new name="your migration name")
endif
	@echo "$(CYAN)Создание новой миграции: $(name)$(RESET)"
	yoyo new ./migrations -m "$(name)"
	@echo "$(CYAN)✓ Миграция создана в ./migrations/$(RESET)"

db.migrate: ## Применить миграции
	@echo "$(CYAN)Применение миграций...$(RESET)"
	yoyo apply --database $(DATABASE_URL) ./migrations
	@echo "$(CYAN)✓ Миграции применены$(RESET)"

db.rollback: ## Откатить последнюю миграцию
	@echo "$(CYAN)Откат миграций...$(RESET)"
	yoyo rollback --database $(DATABASE_URL) ./migrations
	@echo "$(CYAN)✓ Миграция откачена$(RESET)"

db.status: ## Показать статус миграций
	@echo "$(CYAN)Статус миграций:$(RESET)"
	yoyo list --database $(DATABASE_URL) ./migrations

db.up: ## Запустить PostgreSQL в Docker
	@echo "$(CYAN)Запуск PostgreSQL...$(RESET)"
	docker-compose up -d db
	@echo "$(CYAN)Ожидание готовности БД...$(RESET)"
	sleep 5
	@echo "$(CYAN)✓ PostgreSQL запущен$(RESET)"

db.down: ## Остановить PostgreSQL
	@echo "$(CYAN)Остановка PostgreSQL...$(RESET)"
	docker-compose down
	@echo "$(CYAN)✓ PostgreSQL остановлен$(RESET)"

db.logs: ## Показать логи PostgreSQL
	docker-compose logs -f db

db.psql: ## Подключиться к PostgreSQL через psql
	docker-compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

db.clean: ## Удалить данные БД (volumes)
	@echo "$(CYAN)Удаление volumes...$(RESET)"
	docker-compose down -v
	@echo "$(CYAN)✓ Volumes удалены$(RESET)"
