## Getting Started

This project was written using python3.7. A pip requirements.txt
 file is
 included to install the dependencies

## Running with Docker
- A Docker Compose file is provided that will run the application in an
 isolated environment

- Make sure you have `docker & docker-compose` installed and that the Docker
 daemon is running
 
- Build & Run the image: `docker-compose up --build`

- Start using web app: `http://localhost:4200/`

## Running with a virtual environment and NPM

#### Run Django Server

- To run the application in a virtual Python environment, follow these instructions. This example will create a virtual Python environment

- Check you have the pynv version you need:
pyenv versions

- You should see 3.7.6

- If you do not have the correct version of Python, install it like this:
pyenv install 3.7.6

- On command line do this:
~/.pyenv/versions/3.7.6/bin/python -m venv env

- This creates a folder called env. Then do this to activate the virtual environment:
source env/bin/activate

- Lastly do this to check that you are now on the correct Python version:
python --version

To check we are on the right Python version

- You can install the dependencies with `pip install -r requirements/all.txt`

- You can then run the migrations commands with `python manage.py
 makemigrations
` then
 `python manage.py
 makemigrations
` in the weddingshop directory

- You can then run the server command with `python manage.py runserver`

#### Run Angular App 

- Make sure you have Node installed on your machine (v13.11.0 used)

- Run `npm install -g @angular/cli` to install the angular command line tool

To check you have it installed correctly check the version `ng v`

- Install the dependencies by running `npm install` in the src directory

- You can then run the app command with `ng serve`

- Start using web app: `http://localhost:4200/`

## Project Structure Notes

- The Backend Django Rest Framework  are stored in the `weddingshop/weddinglist
` folder
- Project uses sensitive info hardcoded  in `weddingshop/settings` for
 dev purposes only ( store sensitive data are either with environment
  variables or via a json file in production)
- Currently API is for retrieving only as instructed with task
- Django server 'runserver' for dev purposes only, server such a gunicorn for
 prod
 - fixtures to load database with initial data (use tool such celery for prod)
 - The Front-End Angular app are in the `src` folder
 

## API Endpoints using DRF
- Get/Post Users : users/
- PUT/DELETE Users : users/<int:pk>/
- Get/Post Products : products/
- PUT/DELETE Products : product/<int:pk>/
- Get/Post List : list/
- PUT/DELETE List : listitem/<int:pk>/


## Testing
- Run python manage.py test wedding_list.tests # Run test


## Coverage 

```

Module	                   Statements	Missing	Excluded	Coverage
---------------------------------------------------------------
wedding_list/__init__.py	0	0	0	100%
wedding_list/admin.py	        4	0	0	100%
wedding_list/apps.py	        0	0	3	100%
commands/addproducts.py	        15	0	0	100%
wedding_list/models.py	        17	0	0	100%
wedding_list/serializers.py	72	0	0	100%
wedding_list/urls.py	        3	0	0	100%
wedding_list/views.py	        41	0	7	100%
weddingshop/settings.py	        20	0	0	100%
weddingshop/urls.py	        4	0	0	100%
---------------------------------------------------------------
Total	                        399	0	10	100%
```
