# Task description

Write a Python Flask application that presents your CV data:

* As a JSON REST API with endpoints GET /personal, GET /experience, GET /education, ...
* As a Flask CLI command that prints the data to the console

The CV data can be hard-coded in the code or read from disk. You do not need to integrate with any database. Please include a README file on how to start the REST API and how to execute the CLI command.

## Poetry setup

For this task, I've used Poetry as a dependecy and virtual environment manager.
In order to run the project, it needs to be installed by following the steps provided in the [documentation](https://python-poetry.org/docs/#installation).
After installing, the project must be initialized by running the command ```poetry install```, while beeing in the root directory.

## How to run it

The script will be executed directly from the command line and will be provided three arguments in the following order:
```python app.py <local/server> <personal/experience/education> <CV path>```

### Console Output

If we desire the output in the console, the following command needs to be run:
```python app.py local <personal/experience/education/all> <CV path>```

### API Output

If we desire the output as a JSON file, printed in a browser or any API development tool, the following command needs to be run:
```python app.py server <personal/experience/education> <CV path>```
