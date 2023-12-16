FROM python:3.8

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME World
ENV FLASK_APP main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
