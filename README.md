# Demo project

Try for yourself how quickly you can
create a new project with API Bakery.
## Quickstart

1. Set up a Python virtual environment and install the required Python dependencies:

        python3 -m venv <path-to-virtualenv>
        source <path-to-virtualenv>/bin/activate
        pip install -r requirements.txt

2. Create `.env` configuration file based on `env.sample`:

        cp env.sample .env
        vim .env

3. Set up the database

    You'll need to create the database and set `DATABASE_URL` in
    the configuration file before you can run migrations and use the code.

    To use SQLite (supported out of the box), set the `DATABASE_URL` to
    the location of database file (it will be created on the first run),
    either relative to the project directory:

        DATABASE_URL=sqlite:///sqlite.db

    Or absolutely positioned in the file system:

        DATABASE_URL=sqlite:////full/path/to/sqlite.db

    (Note the three or four dashes in the URL, respectively).

    To use PostgreSQL or MariaDB databases, install the appropriate
    driver and create database and user as needed. Example for
    PostgreSQL (this assumes you already have PostgreSQL installed
    on your system via package manager such as apt, rpm, or brew):

    1. Connect to the database as admin and create a new user and database

        CREATE USER 'appuser' WITH PASSWORD 'secretpassword';
        CREATE DATABASE 'dbname' WITH OWNER 'appuser';

    2. Install Python database driver for PostgreSQL

        pip install psycopg2

    3. Set up `DATABASE_URL` in your `.env`:

        DATABASE_URL=postgres://appuser:secretpassword@localhost/dbname

4. Run migrations:

        python manage.py migrate

4. Run the server:

        python manage.py runserver

5. Visit the browsable API at http://localhost:8000/api/v1/

6. Access the Django admin at http://localhost:8000/admin/

## Creating superuser

A superuser account can be created using the Django management command:

    python manage.py createsuperuser


## Running tests

    python manage.py test


## Docker support

Build the docker image with:

        docker build -t demo-project .

The default command is to start the web server (gunicorn). Run the image
with `-P` docker option to expose the internal port and check the exposed
port with `docker ps`:

        docker run --env-file .env --P demo-project
        docker ps

Make sure you provide the correct path to the env file (this example assumes
it's located in the local directory).

To run a custom command using the image (for example, db migrations):

        docker run --env-file .env demo-project python manage.py migrate

To run a Django shell inside the container:

        docker run --env-file .env -t demo-project

Note that any changes inside the container will be lost. For that reason,
running `collectstatic` or using a SQLite database within a container will
have no effect. If you want to use SQLite with docker, mount a docker
volume and place the SQLite database inside it.

For more information on the docker build process, see the included `Dockerfile`.