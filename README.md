# SI 664 Project folder

## Prerequistes

1. install python
2. install the django library
3. install ngrok in your file system root
4. install project dependencies with `pip install -r requirements.txt`

## Commands

### Run the project

1. `python manage.py runserver`
2. open terminal at root and run `./ngrok http 8000`

### Create a New Site (which can contain many applications)

- `django-admin startproject mysite`

### Create a new application

- `python manage.py startapp <APP_NAME>`

### Check for syntax errors

- `python manage.py check`

### When making changes to a model, migrate those changes

- `python manage.py makemigrations <APP_NAME>`
- `python manage.py migrate`

### Invoke the Python shell

- `python manage.py shell`

### Run a script

- `python manage.py runscript <SCRIPT.py>`

### Create a Superuser

- `python manage.py createsuperuser`

## When working in PythonAnywhere

### When you create a new console - start the virtual environment

- `workon python3`

Note: You can also launch the console from the web which will automatically lauch the virtual env.

## To Do [priority]

- [high] Fix the food scrape, fragments, better/other names (maybe descritptions), get scientific names. Add categories, dont over writes

- [high] Do not write over the Wiki food. Create a separate object for the pairing with all new fields.

- [medium] Store more images from both wikipedia and unsplash with as much metadata as possible

- [low] Find other photo APIs

- [low] auto crop images?

- [low] Identify best images (after more features can be aggrgated)

- [low] Somehow combine results for the same foods but from different dataTypes
