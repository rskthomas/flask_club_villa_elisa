# Make it work with docker

You can use docker-compose file store at root folder of the repository. Then you run

1. `docker compose build` for building docker image
2. `docker compose run web poetry run flask database reset` to set up you db (and anytime you want to create DB based on sql achemy models)
3. `docker compose up web`
4. Voilà. Your flask app is running at [port 5001](http://localhost:5001)