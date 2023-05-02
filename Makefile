image:
	docker build -t reservai:latest .

run:
	docker run -p 8080:8080 reservai:latest

fe-dev:
	cd frontend; yarn dev

fe-build:
	cd frontend; yarn build

server:
	uvicorn src.main.main:app

server-watch:
	uvicorn src.main.main:app --reload