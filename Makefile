coverage:
	pip install -r requirements_dev.txt
	python -m pytest --cov=fastapi_example tests/ --cov-report term-missing

test:
	pip install -r requirements_dev.txt
	python -m  pytest .
	isort . --line-length 120 -q --diff


build: test
	docker build -t fastapi-example:latest .


run:
	docker run -it --publish 3000:3000 fastapi-example:latest
