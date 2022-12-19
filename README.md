# Personal Expense Tracker Assessment

## Description 
This is a sample Personal Expense Tracker based on the OpenAPI 3.0 specification. Design an API to be used to track a user's expenses. This implementation should be as simple as possible, but still exhaustive enough to showcase most API principles.

## Introduction
This is a sample Personal Expense Tracker based on the OpenAPI 3.0 specification. Design an API to be used to track a user's expenses. This implementation should be as simple as possible, but still exhaustive enough to showcase most API principles.

## Running the code locally
* Create a virtual environment
* Clone the project 
* Install required dependencies with `pip install -r requirements.txt`
* Run migrations (Migrations should already exist) with `python manage.py migrate`
* Run the local server with `python manage.py runserver`
* Visit the Swagger API documentation on `http://localhost:8080/api/docs/`
* Create a superuser with `python manage.py createsuperuser` and fill out the information in the prompt
* Login to the admin in the browser via `http://localhost:8080/admin/`
* To run tests, run `python manage.py test`



## Running via Docker Compose
* Clone the project
* Make sure docker and docker-compose are installed on your system
* From the root of the project run the following to build and start `docker-compose up --build`
* Once the container starts, access the Swagger API documentation via `http://localhost:8032/api/docs/`
* Run the following command to create a superuser `docker-compose exec -it app python manage.py createsuperuser` and follow the prompt
* To run the tests, run `docker-compose exec -it app python manage.py test`
* PostgreSQL is used and the exposed on port 5435 on localhost

#### End
