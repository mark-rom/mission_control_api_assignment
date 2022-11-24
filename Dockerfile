FROM python:3.10-slim

WORKDIR /app

COPY ./ /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

CMD ["gunicorn", "space_stations.wsgi:application", "--bind", "0:8000" ]