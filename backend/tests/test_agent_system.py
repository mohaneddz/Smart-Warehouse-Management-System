from core.agent_system import Agent
from core.warehouse import Node

def test_agent_movement():
    node1 = Node(0, 0)
    node2 = Node(1, 0)
    agent = Agent(node1, weight=1.0, state="idle", goal="A")

    agent.move(node2)
    assert agent.node == node2
