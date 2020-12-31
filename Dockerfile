FROM python:3.8.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . /app

RUN brownie compile

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
