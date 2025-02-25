# nebula
A toolkit for [Project Electron](http://projectelectron.rockarch.org/) Postgres-backed Django microservices.

## What's here

- `.travis.yml` - Travis CI configuration (useful when you push code to GitHub)
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Docker Compose configuration
- `entrypoint.sh` - A script which runs after the container starts up. If you want to add default objects or users, this is a good place to do it.
- `requirements.in` - Minimal Python package requirements.
- `wait-for-it.sh` - Tests if a TCP host and port are available, useful if you need to wait for a service to start up completely.

## Requirements

Using this repo requires having [Docker](https://store.docker.com/search?type=edition&offering=community) installed.

## Getting started

Clone the repository to a new directory:

    $ git clone git@github.com:RockefellerArchiveCenter/nebula.git new_project

Move to the root directory of the repository:

    cd new_project/

Update the requirements file. First, pin the specific versions of the packages you want to use in `requirements.in` and then, with [pip-tools](https://github.com/jazzband/pip-tools) installed, run `pip-compile`. This command will generate a `requirements.txt` file with all the dependencies necessary for your project.

Create a new Django project by running `django-admin.py` in the Docker container, replacing "new_project" with the name of the new service you are building:

    docker-compose run web django-admin.py startproject new_project .

Uncomment the `entrypoint` key in `docker-compose.yml`, and still in the root directory, run docker-compose:

    $ docker-compose up

Once the application starts successfully, you should be able to access it in your browser at `http://localhost:8000`

When you're done, shut down docker-compose:

    $ docker-compose down


### Other things you'll want to do:
- Rename services in the docker-compose file so they have slightly less generic names.
- Create a file called `config.py` in the main project directory to store local variables, and add it to `.gitignore`. You should add private settings to this file; see other Project Electron Django apps for examples.
- Create a file called `config.py.example` which mirrors the structure of `config.py`. This helps to document which configs are required, and can also be used for automated unit testing.
- Point your database at the Postgres database running as a separate service.
- With [pre-commit](https://pre-commit.com/) installed, run `pre-commit install` to add git pre-commit hooks to your CI pipeline.
- Update the default values for the ports exposed in `docker-compose.yml` for local development.
- Update the value of the `DJANGO_PORT` variable in `.travis.yml` for the deployed application.
- Update the `CONTAINER`, `APPLICATION_NAME` variables in `.travis.yml` and uncomment out the commented job steps.
- Add Travis CI environment variables for `DOCKER_USERNAME` and `DOCKER_PASSWORD` in the UI at <https://travis-ci.com>.
- Before pushing code, remember to change your remotes!

## License

Code is released under an MIT License, as all your code should be. See [LICENSE](LICENSE) for details.
