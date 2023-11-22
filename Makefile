# Makefile

NAME = python-bot

ENV_PATH = ./app/telegram_ai/.env

TELEGRAM_API_KEY=
OPENAI_API_KEY=

ifndef TELEGRAM_API_KEY
	$(error TELEGRAM_API_KEY is not set)
endif

ifndef OPENAI_API_KEY
	$(error OPENAI_API_KEY is not set)
endif

update-env:
	sed -i 's/^\(TELEGRAM_API_KEY=\).*/\1'$(TELEGRAM_API_KEY)'/' $(ENV_PATH)
	sed -i 's/^\(OPENAI_API_KEY=\).*/\1'$(OPENAI_API_KEY)'/' $(ENV_PATH)

build:
	docker build -t python-bot ./app/

up:
	docker compose up -d

down:
	docker compose down

$(NAME): update-env build up

all: $(NAME)
