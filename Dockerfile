FROM python:3.11-alpine

WORKDIR /movies

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "movies.py"]