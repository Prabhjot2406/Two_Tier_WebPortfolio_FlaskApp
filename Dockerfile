FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt 
RUN apt-get update && apt-get install -y sqlite3
ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0 
CMD ["flask", "run"]
