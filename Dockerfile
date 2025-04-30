FROM python:latest

WORKDIR .

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "x.wsgi", "-b", "0.0.0.0:8000"]