FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /src/

RUN apt-get update

WORKDIR /src

RUN pip install -r requirements.txt

ENV FLASK_APP=app.api

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]