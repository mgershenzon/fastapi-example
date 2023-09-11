# fastapi-example
Example project with a few simple APIs that don't do much and pytests to check them.


# Requirements

You can install just the basic ones and still work on the code.

However, it is also recommended to install the advanced items.
It will make it easier to work, plus the rest of this page assumes you did so.


## Basic
* Python (tested on python 3.11.3)

You can just install python and run with:

```markdown
PYTHONPATH=. python ./fastapi_example/main.py 
```

## Advanced

* Docker
* Make


Warning -
This was written and tested on MacOS, so some things may not work on Linux/Windows.

# How to run:

After cloning the repo and going inside the directory, you can use the makefile commands  

## Option 1 - Running in a docker container
```
make build  
make run  
```
Then open the next link in the browser http://localhost:3000/

## Option 2 - Running the python script directly on your operating system
```
make python
```
Then open the next link in the browser http://localhost:80/


# How to work with requirements file
The requirements.txt file is the one needed for running in production.
When building the docker image, it's the one used.

The requirements_dev.txt file is for running pytext and checking coverage etc.

Both are in a tree structure generated with pipdeptree.

## Cleaning the env

To delete all the python libraries from the environment:
```
make pip_uninstall
```
## Upgrade libraries

To upgrade the top level libraries for the requirements.txt file use:
```
make pip_upgrade
```

or for the requirements_dev.txt file use:

```
make pip_upgrade_dev
```

It will change the libraries installed, but not the code.
To change the code, copy the new dependency tree from the output to relevant file.


## Adding/Removing dependencies
1. Start from a clean environment `make pip_uninstall`
2. Install the requirements.txt file `make pip_install`
3. If the change is in the requirements_dev.txt file, also run `make test`
4. Add/Remove your dependencies using pip
5. Run `make freeze` and paste the new tree to the requirement file


## Useful make targets
* `make help` prints all available make targets
* `make test` run the py-tests after installing the dev requirements. This also checks the import order.
* `make coverege` check the coverage after installing the dev requirements (it should be 100%).


## Few words about the code
The main script is here: fastapi_example/main.py
Configuration is here: /fastapi_example/config.py

If you want to add fastapi routers, there should be under `fastapi_example/api`
And should be added to the main router in `fastapi_example/api/group_routers.py` 