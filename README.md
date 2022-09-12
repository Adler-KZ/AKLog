# AKLog project
Check out the [project](https://aklog.herokuapp.com/).
## Want to use this project?

1. Rename `.env-sample` to `.env`:

2. Update the environment variables in `.env` file.

3. Build the images and run the containers:

        docker-compose up -d --build

4. Run migrations:

        docker-compose run web python manage.py migrate


5. Test it out at http://localhost:8000

