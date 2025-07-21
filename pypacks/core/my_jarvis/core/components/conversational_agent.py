from abc import ABC, abstractmethod

class ConversationalAgent(ABC):
    @abstractmethod
    def query(self, message: str) -> str:
        """Process a message and return a response."""
        pass

class EchoConversationalAgent(ConversationalAgent):
    def query(self, message: str) -> str:
        return message
