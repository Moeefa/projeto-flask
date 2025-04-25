.PHONY: make up down build logs status

make:
	@echo "Comandos disponíveis:"
	@echo "  up      - Sobe os serviços"
	@echo "  down    - Derruba os serviços"
	@echo "  build   - Constrói os serviços"
	@echo "  logs    - Mostra logs em tempo real"
	@echo "  status  - Lista os containers"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

status:
	docker compose ps

