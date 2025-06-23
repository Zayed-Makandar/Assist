from .provider import AIProviderBase

class QwenProvider(AIProviderBase):
    def ask(self, prompt):
        # TODO: Implement real Qwen API call
        return f"Qwen would answer: {prompt}"