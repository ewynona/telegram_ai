import openai

openai.api_key = "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"


class GptCharacter:
    def __init__(self, character):
        self.character = character
        self._messages = []
        self._messages.append({"role": "system", "content": f"You should not say that you are a computer program, "
                                                            f"a bot, an artificial intelligence. "
                                                            f"All your answers must be from {self.character}"})

    def set_message(self, message):
        self._messages.append({"role": "user", "content": message})

    def set_bot_message(self, message):
        self._messages.append({"role": "assistant", "content": message})

    def get_message(self):
        response = self._generate_response()
        reply = response["choices"][0]["message"]["content"]
        self._messages.append({"role": "assistant", "content": reply})
        return reply

    def _generate_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages,
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def get_msg(self):
        return self._messages
