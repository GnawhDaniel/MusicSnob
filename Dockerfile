FROM python:3.14 AS dev
WORKDIR /code
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY .env /code/.env
EXPOSE 5001
CMD ["fastapi", "dev", "./engine/server.py", "--host", "0.0.0.0", "--port", "5001"]

FROM python:3.14 AS prod
WORKDIR /code
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY .env /code/.env
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh
EXPOSE 5001
ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["uvicorn", "engine.server:app", "--host", "0.0.0.0", "--port", "5001"]
