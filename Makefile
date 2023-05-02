image:
	docker build -t reservai:latest .

run:
	docker run -p 8080:8080 reservai:latest

fe-dev:
	cd frontend; yarn dev

fe-build:
	cd frontend; yarn build

server:
	cd src; uvicorn main.main:app

server-watch:
	cd src; uvicorn main.main:app --reload

test:
	cd src; python3 -m pytest tests/integration/