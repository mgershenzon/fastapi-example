# FastAPI Example Project

This is an example project showcasing several simple APIs alongside corresponding Pytest tests to validate their functionality.

## Prerequisites

You have the flexibility to install only the basic prerequisites and still engage with the code. However, we highly recommend installing the advanced prerequisites, as they significantly enhance the development experience. This documentation assumes that you have installed the advanced ones.

### Basic Prerequisites

- Python (tested on Python 3.12.1)

Once you have installed Python, you can effortlessly execute the project using the following command:

```bash
PYTHONPATH=. python ./fastapi_example/main.py
```

### Advanced Prerequisites (Optional)

- Docker
- Make

**Warning:** This project was developed and tested on MacOS, which means that certain features may not work seamlessly on Linux or Windows.

## How to Run

After cloning the repository and navigating to its directory, you can utilize the provided Makefile commands to run the project.

### Option 1 - Running in a Docker Container

```bash
make build
make run
```

Then, open the following link in your web browser to check it out: [http://localhost:3000/](http://localhost:3000/)

### Option 2 - Running the Python Script Directly on Your Operating System

```bash
make python
```

Then, open the following link in your web browser to check it out: [http://localhost:80/](http://localhost:80/)

## Managing Requirement Files

This project comprises two requirement files:

- `requirements.txt`: This file includes only the essentials needed to run the project in a production environment and is used during the Docker image building process.
- `requirements_dev.txt`: This file serves for running Pytests, checking code coverage, and handling other development-related tasks.

Both files are generated with a tree structure using `pipdeptree`.

### Cleaning the Environment

To remove all Python libraries from the environment:

```bash
make pip_uninstall
```

### Upgrading Libraries

To upgrade the top-level libraries and all their dependencies while getting rid of the old requirements that are no longer needed in the `requirements.txt` file, employ:

```bash
make pip_upgrade
```

For the `requirements_dev.txt` file, use:

```bash
make pip_upgrade_dev
```

These commands update the installed libraries without altering the code. To modify the code, copy the new dependency tree from the output to the relevant file.

### Adding/Removing Dependencies

1. Begin with a clean environment: `make pip_uninstall`
2. Install the `requirements.txt` file: `make pip_install`
3. If the change pertains to the `requirements_dev.txt` file, also execute: `make test`
4. Add or remove your dependencies using `pip`.
5. Execute `make freeze` and insert the new tree into the relevant requirement file.

## Useful Make Targets

- `make help`: Displays all available make targets.
- `make test`: Executes Pytests after installing the development requirements, including verification of the import order.
- `make coverage`: Validates the test coverage after installing the development requirements; it should achieve 100%.

## Insights into the Code

- **Main Script:** `fastapi_example/main.py`
- **Configurations:** `fastapi_example/config.py`

  Here you can configure the port, number of workers in the app, enable json log format and much more.
- **Project Makefile:** `Makefile`

  Useful commands that can be run with `make`, or used as a cheatsheet.
- **API Endpoints:** `fastapi_example/api/routes/*`

  These files represent the heart of the application, defining how it responds to various requests. Each function with a path annotation acts as an individual endpoint. Adding a new endpoint is simple: create a function here and specify its path.
- **FastAPI Top Level Route:** `fastapi_example/api/group_routers.py`
  This file acts as a traffic manager, organizing all the routes in to one route, that will be used by the application.
  
To add a new endpoint to the application:
1. Open one of the files under `fastapi_example/api/routes`
2. Create a new function and annotate it with the desired path (e.g., `@router.get('/new_endpoint')`).
3. That's it. Run the server, and you can call your new endpoint.
 
Bonus: If you wish to add a new file that will contain endpoints under `fastapi_example/api/routes`, you can. Just create it, instantiate a new router and add the new router to  `fastapi_example/api/group_routers.py`.