Q_ARGUMENT := ""
EMPTY_OR_DEV_ARGUMENT := ""

help:				## Show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

which:				## Some info. Useful when running from IDE gives different results compared to the terminal.
	which python
	which pip
	which docker
	date


pip_install:		 ## Install requirements.txt
	pip install -r requirements.txt


freeze:				## Freeze dependencies in a tree format
	pip install -qqq pipdeptree
	@echo
	pipdeptree -fl -e pip,setuptools,pipdeptree,wheel
	@echo
	pip uninstall -yqqq pipdeptree


pip_uninstall:		## Uninstall all the that returns from `pip freeze`
	@eval "pip freeze | xargs pip uninstall -y $(Q_ARGUMENT)"


pip_upgrade:		## Upgrade all the dependencies in the requirements file. Careful, it will first call pip_uninstall.
	$(MAKE) Q_ARGUMENT="-qqq" pip_uninstall
	@echo "Uninstalling finished. Getting ready to install latest..."
	@echo
	@eval "cat requirements$(EMPTY_OR_DEV_ARGUMENT).txt | sed 's/==.*//g' | sed '/  .*/d' | xargs -I{} pip install -qqqU {};"
	$(MAKE) freeze


pip_upgrade_dev:	## Upgrade all the dependencies in the requirements_dev file. Careful, it will first call pip_uninstall.
	$(MAKE) EMPTY_OR_DEV_ARGUMENT="_dev" pip_upgrade


coverage:			## Check coverage after installing requirements_dev
	pip install -r requirements_dev.txt
	python -m pytest --cov=fastapi_example tests/ --cov-report term-missing


test:				## Run all the tests after installing requirements_dev
	pip install -r requirements_dev.txt
	python -m  pytest .
	isort . --line-length 120 -q --diff


python:				## Run the python module directly
	$(MAKE) pip_install
	PYTHONPATH=. python ./fastapi_example/main.py


build:				## Build docker image from code
	$(MAKE) test
	docker build --build-arg=GIT_COMMIT=$(shell git describe --match= --always --abbrev=40 --dirty) --build-arg=BUILD_URL=$(shell HOSTNAME) --build-arg=BUILD_ID=LOCAL_BUILD --build-arg=BUILD_NUMBER=LOCAL_BUILD -t fastapi-example:latest .


run:				## Run the latest docker image
	docker run -it --publish 3000:80 fastapi-example:latest
