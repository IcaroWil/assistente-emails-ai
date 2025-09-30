.PHONY: install run test docker-build docker-run

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r backend/requirements.txt

run:
	. .venv/bin/activate && uvicorn backend.uvicorn_app:app --reload

test:
	. .venv/bin/activate && pytest -q

docker-build:
	docker build -t email-ai-classifier:latest .

docker-run:
	docker run -p 8000:8000 email-ai-classifier:latest
