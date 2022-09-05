FROM python:3-alpine

RUN apk update

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "bot.py" ]