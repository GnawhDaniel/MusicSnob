FROM python:3.14

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./engine /code/engine/
COPY ./internal /code/internal
COPY .env /code/.env
COPY ./db /code/db

EXPOSE 5001

CMD ["uvicorn", "engine.server:app", "--host", "0.0.0.0", "--port", "5001"]