FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app/
ENV DB_HOST database
COPY . .
RUN python3 -m pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000