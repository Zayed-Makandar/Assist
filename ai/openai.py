from .provider import AIProviderBase

class OpenAIProvider(AIProviderBase):
    def ask(self, prompt):
        # TODO: Implement real OpenAI API call
        return f"OpenAI would answer: {prompt}"