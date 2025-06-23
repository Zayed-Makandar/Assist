from .provider import AIProviderBase

class MockProvider(AIProviderBase):
    def ask(self, prompt):
        return f"Mock response to: {prompt}"