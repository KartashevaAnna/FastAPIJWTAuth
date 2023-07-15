FROM python:3.11
WORKDIR /fastapi
COPY requirements.txt /fastapi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /fastapi

CMD ["uvicorn", "docker_app:app", "--host", "0.0.0.0", "--port", "80"]
