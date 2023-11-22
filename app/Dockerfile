FROM python:3.10.13-bookworm

RUN apt update && apt upgrade -y

WORKDIR /python-bot

COPY ./telegram_ai ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]