FROM python:3.8.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ENV HOME /app

COPY ./network-config.yaml $HOME/.brownie/network-config.yaml
COPY ./brownie-config.yaml /app
COPY ./contracts /app/contracts
COPY ./interfaces /app/interfaces

RUN brownie compile

COPY . /app

ENTRYPOINT [ "gunicorn" ]

CMD [ "-b", "0.0.0.0:5000", "app:app" ]
