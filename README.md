# Weather API

## Set up

The first thing to do is to clone the repository:
```
$ git clone https://github.com/johnnyvargast/weather-api.git
$ cd weather-api
```

## Running

### Using `Virtual Environment`
- Python 3.7
- PIP (package manager) (pip v19.0.3)
- Virtual Environment (pipenv or virtualenv)


Create a virtual environment to install dependencies in and activate it.
```
$ virtualenv weather-env
$ source weather-env/bin/activate
```
Then install the dependencies:
```
$ pip install -r requirements.txt
```
Create the `.env` file in the main project folder.

Set up the `.env` file with corresponding variables like `secrete_key`. You can use the `.env.example` file as a guide.

After all these steps , you can run this project with the command.

```
python manage.py runserver
```
And navigate to http://127.0.0.1:8000/

---

### Using `docker`

You can also use docker directly and use the following commands:

```
$ docker build -t weather_api .
$ docker run --rm -t -p 9000:9000 --env-file .env weather_api
```

### Using `docker-compose`

```
docker-compose up --build
```

And navigate to http://127.0.0.1:9000/

---

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
$ python manage.py test
```