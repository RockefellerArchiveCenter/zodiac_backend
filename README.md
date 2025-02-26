# zodiac_backend
A backend API for tracking ingest of digital packages.

## Setup

Install [git](https://git-scm.com/) and clone the repository

    $ git clone git@github.com:RockefellerArchiveCenter/zodiac_backend.git

Install [Docker](https://store.docker.com/search?type=edition&offering=community) and run docker-compose from the root directory

    $ cd zodiac_backend
    $ docker compose up

Once the application starts successfully, you should be able to access the application in your browser at `http://localhost:8000`

When you're done, shut down docker-compose

    $ docker compose down

Or, if you want to remove all data

    $ docker compose down -v


## Configuring

Argo configurations are stored in `/zodiac_backend/config.py`. This file is excluded from version control, and you will need to update this file with values for your local instance.

The first time the container is started, the example config file (`/zodiac_backend/config.py.example`) will be copied to create the config file if it doesn't already exist.


## Routes

| Method | URL | Parameters | Response  | Behavior  |
|--------|-----|---|---|---|
|GET|/events|outcome, service|200|Returns data about all Events|
|GET|/events/{event_id}||200|Returns data about an Event|
|POST|/events||201|Creates Event data|
|PUT|/events/{event_id}||200|Updates Event data|
|GET|/packages|origin|200|Returns data about all Packages|
|GET|/packages/{package_id}|origin|200|Returns data about a Package|
|GET|/packages/{package_id}/events|origin|200|Returns data about Events associated with a Package|
|POST|/packages|origin|200|Creates Package data|
|PUT|/packages/{pacakge_id}||200|Updates Package data|


## Development

This repository contains a configuration file for git [pre-commit](https://pre-commit.com/) hooks which help ensure that code is linted before it is checked into version control. It is strongly recommended that you install these hooks locally by installing pre-commit and running `pre-commit install`.

## License

Code is released under an MIT License, as all your code should be. See [LICENSE](LICENSE) for details.
