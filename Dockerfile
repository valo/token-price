FROM python:3.8.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ENV HOME /app

COPY ./network-config.yaml $HOME/.brownie/network-config.yaml

COPY . /app

RUN brownie compile

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]