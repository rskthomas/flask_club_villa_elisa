FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /var/www

ENV STATIC_URL /public
ENV STATIC_PATH /var/www/app/static \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin" \
    POETRY_VERSION=1.2.0 \
    FLASK_APP='/var/www/app.py'

RUN pip install poetry

COPY poetry.lock pyproject.toml /var/www/

EXPOSE 5000

RUN cd /var/www && poetry config virtualenvs.create false
RUN cd /var/www && poetry install --no-dev --no-root --no-interaction --no-ansi
RUN apt-get update && apt-get install -y wkhtmltopdf


CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]