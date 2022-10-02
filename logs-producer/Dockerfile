FROM python:3.8

RUN pip install "poetry"
WORKDIR /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD [ "python", "main.py" ]