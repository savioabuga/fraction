##  App

A project created as part of the Fraction job interview progress.

This is a web app built using django. 

## Technologies used

1. Django for the backend

2. Postgres with postgis for the database

3. Docker and docker-compose for containerization od the app

5. [Django Chartit](https://github.com/chartit/django-chartit) for charts

6. [Smartmin](https://github.com/nyaruka/smartmin) for CRUDL operations.

## Usage

To start the application:

* Unzip or git clone it and change directory to the `fraction` directory.

* The run the following command.

```bash
    docker-compose up -d --build

```

* After the application has finished installing all requirements and started running, you can access it on your browser [http://localhost:8004/](http://localhost:8004/)

## Troubleshooting

You can check any issues by following the logs with the following command:

```bash
docker-compose logs -f --tail=50
```

## TODO

- [ ] Add Gunicorn and Nginx to the application to serve backend and client.

- [ ] Generating new credentials and moving them from the repo. Using something like [envkey](https://www.envkey.com/) to store credentials.

- [ ] Adding docker and docker-compose files for various environment.

- [ ] Introducing CI/CD.

## License
[MIT](https://choosealicense.com/licenses/mit/)