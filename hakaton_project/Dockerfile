FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /hakaton_project

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py loaddata sample.json

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
