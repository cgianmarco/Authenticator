FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev default-libmysqlclient-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]