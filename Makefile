Q_ARGUMENT := ""
EMPTY_OR_DEV_ARGUMENT := ""
REQ_IN := requirements.in
REQ_TXT := requirements.txt
DEV_PREFIX := tests/dev_


help:				## Show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


which:				## Some info. Useful when running from IDE gives different results compared to the terminal.
	which python
	which pip
	which docker
	date


pip_install:		 ## Install requirements.txt
	pip install -r $(EMPTY_OR_DEV_ARGUMENT)$(REQ_TXT)


pip_uninstall:		## Uninstall all that returns from `pip freeze`
	@eval "pip freeze | xargs pip uninstall -y $(Q_ARGUMENT)"


freeze_tree:		## Freeze dependencies in a tree format (based on mandatory requirements)
	pip install -qqq pipdeptree
	@echo
	pipdeptree -fl -e pip,setuptools,pipdeptree,johnnydep,wheel,packaging
	@echo
	pip uninstall -yqqq pipdeptree


req_in_upgrade:		## Upgrade dependencies in requirements.in and install. Doesn't change requirements.txt
	sed -I '' 's/[=<>].*//g' $(EMPTY_OR_DEV_ARGUMENT)$(REQ_IN)
	pip install -r $(EMPTY_OR_DEV_ARGUMENT)$(REQ_IN)
	cat $(EMPTY_OR_DEV_ARGUMENT)$(REQ_IN) | grep -v '$(REQ_IN)'| xargs -I{} bash -c "pip freeze| grep -E '^{}=='" > tmp && mv tmp $(EMPTY_OR_DEV_ARGUMENT)$(REQ_IN)


req_in_upgrade_dev:	## Upgrade dependencies in tests/dev_requirements.in and install. Doesn't change tests/dev_requirements.txt
	$(MAKE) EMPTY_OR_DEV_ARGUMENT="tests/dev_" req_in_upgrade
	echo "-r ../requirements.in" | cat - $(DEV_PREFIX)$(REQ_IN) > tmp && mv tmp $(DEV_PREFIX)$(REQ_IN)


upgrade:			## Upgrade in files versions and generate requirements txt files, then install requirements.txt
	$(MAKE) Q_ARGUMENT="-qqq" pip_uninstall
	@echo "Uninstalling finished. Getting ready to upgrade to latest..."
	pip install pip-tools
	@echo
	$(MAKE) EMPTY_OR_DEV_ARGUMENT='' req_in_upgrade
	pip-compile requirements.in
	@echo "Done compiling requirements.in"
	$(MAKE) req_in_upgrade_dev
	pip-compile tests/dev_requirements.in
	@echo "Done compiling tests/dev_requirements.in"
	$(MAKE) Q_ARGUMENT="-qqq" pip_uninstall
	@echo Installing from requirements file
	$(MAKE) pip_install


upgrade_dev:		## Upgrade in files versions and generate requirements txt files, then install dev_requirements.txt
	$(MAKE) EMPTY_OR_DEV_ARGUMENT=$(DEV_PREFIX) upgrade


compile:			## Recompile requirements files
	pip install pip-tools
	pip-compile requirements.in
	pip-compile tests/dev_requirements.in


coverage:			## Check coverage after installing tests/dev_requirements
	$(MAKE) EMPTY_OR_DEV_ARGUMENT=$(DEV_PREFIX) pip_install
	python -m pytest --cov=fastapi_example tests/ --cov-report term-missing


test:				## Run all the tests after installing tests/dev_requirements
	$(MAKE) EMPTY_OR_DEV_ARGUMENT=$(DEV_PREFIX) pip_install
	python -m pytest -n 4 --durations=0 .
	isort . --line-length 120 -q --diff


python:				## Run the python module directly
	$(MAKE) pip_install
	PYTHONPATH=. python ./fastapi_example/main.py


build:				## Build docker image from code
	$(MAKE) test
	docker build --build-arg=GIT_COMMIT=$(shell git describe --match= --always --abbrev=40 --dirty) --build-arg=BUILD_URL=$(shell HOSTNAME) --build-arg=BUILD_ID=LOCAL_BUILD --build-arg=BUILD_NUMBER=LOCAL_BUILD -t fastapi-example:latest .


run:				## Run the latest docker image
	docker run -it --publish 3000:80 fastapi-example:latest
