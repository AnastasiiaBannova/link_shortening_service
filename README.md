Short link generation service
=============================

Local development
-----------------

To run server locally - `docker-compose up`

To run migrations`docker-compose exec web_app alembic upgrade head` to run migrations

It will run development server on `http://0.0.0.0:8000`

To run tests and linters - `tox`