FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y ffmpeg

RUN apt install -y python3-dev


RUN python3 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input

RUN chmod -R 755 /static

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
