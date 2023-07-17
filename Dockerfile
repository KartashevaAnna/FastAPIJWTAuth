FROM python:3.11-slim

WORKDIR /fastapi
COPY requirements.txt /fastapi
RUN apt-get update

RUN pip install -r requirements.txt


COPY .. /fastapi
COPY app /fastapi


#CMD ["uvicorn", "docker_run:app", "--host", "0.0.0.0", "--port", "80"]