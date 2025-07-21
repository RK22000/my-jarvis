from .conversational_agent import ConversationalAgent, EchoConversationalAgent

class Playground:
    def __init__(self):
        self._conversational_agent: ConversationalAgent = EchoConversationalAgent()

    @property
    def conversational_agent(self) -> ConversationalAgent:
        return self._conversational_agent
