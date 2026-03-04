.PHONY: help up down logs clean init create-user

help:
	@echo "Доступные команды:"
	@echo "  make up           - Запустить все сервисы"
	@echo "  make down         - Остановить сервисы"
	@echo "  make logs         - Показать логи"
	@echo "  make clean        - Удалить все данные"
	@echo "  make init         - Инициализация БД"
	@echo "  make create-user  - Создать admin пользователя"

up:
	mkdir -p ./dags ./logs ./plugins
	docker-compose up -d
	@echo "Ожидание запуска сервисов..."
	@sleep 20
	@echo "✅ Airflow запущен: http://localhost:8080"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-webserver:
	docker-compose logs -f airflow-webserver

logs-scheduler:
	docker-compose logs -f airflow-scheduler

logs-db:
	docker-compose logs -f postgres

clean:
	docker-compose down -v
	sudo rm -rf ./logs/*
	@echo "✅ Все данные удалены"

init:
	docker-compose up airflow-init

create-user:
	docker-compose exec airflow-webserver airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com

restart:
	docker-compose restart

ps:
	docker-compose ps
