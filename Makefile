pip_install:
	pip install -r requirements.txt


freeze:
	@ pip install -qqq pipdeptree
	pipdeptree -fl -e pip,setuptools,pipdeptree
	@ pip uninstall -yqqq pipdeptree


pip_uninstall:
	pip freeze | xargs pip uninstall -y


coverage:
	pip install -r requirements_dev.txt
	python -m pytest --cov=fastapi_example tests/ --cov-report term-missing


test:
	pip install -r requirements_dev.txt
	python -m  pytest .
	isort . --line-length 120 -q --diff


build: test
	docker build --build-arg=GIT_COMMIT=$(shell git describe --match= --always --abbrev=40 --dirty) --build-arg=BUILD_URL=$(shell HOSTNAME) --build-arg=BUILD_ID=LOCAL_BUILD --build-arg=BUILD_NUMBER=LOCAL_BUILD -t fastapi-example:latest .


run:
	docker run -it --publish 3000:80 fastapi-example:latest
