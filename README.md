# Telegram AI

Telegram AI - это мой аналог сайта character_ai. Вы можете выбрать предоставленного персонажа и начать общение с ним через Telegram.

## Запуск

1. Нужно задать ключи TELEGRAM_API_KEY и OPENAI_TELEGRAM_KEY внутри Makefile
2. Собрать образ: make python-bot

Если возникают трудности с получением api ключа openai, в хедлере cmd_text вместо генерации ответа от chatgpt стоит заглушка

