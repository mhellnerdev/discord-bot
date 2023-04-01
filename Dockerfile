FROM python:3.7.13-alpine3.16

RUN apk update

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "bot.py" ]