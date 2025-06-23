import openai
from config import OPENAI_API_KEY

class OpenAIAssistant:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def ask(self, prompt):
        # Construct messages as required by OpenAI API
        messages = [
            {
                "role": "system",
                "content": "You are Assist, a helpful and friendly AI assistant for Windows. Answer clearly and concisely."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        # Use the client to create a chat completion
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content

def get_ai_provider(provider_name):
    if provider_name.lower() == "openai":
        return OpenAIAssistant(OPENAI_API_KEY)
    raise ValueError(f"Unknown AI provider: {provider_name}")