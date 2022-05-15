FROM python:slim

ADD static /app/static/
ADD templates /app/templates/
ADD ./main.py /app/main.py
ADD ./requirements.txt .
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "/app/main.py"]
