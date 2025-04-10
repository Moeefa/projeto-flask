hello:
	echo "hello world"

up:
	docker compose up -d --build

down:
	docker compose down