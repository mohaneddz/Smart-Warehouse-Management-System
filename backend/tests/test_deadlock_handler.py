import unittest
from core.agent_system import Agent
from core.warehouse import Node
from utils.deadlock_handler import DeadlockHandler

class TestDeadlockHandler(unittest.TestCase):
    def test_deadlock_detection(self):
        # Create two agents that are in a blocked state (example)
        agent1 = Agent(node=Node(0, 0), weight=10, state="blocked", goal="pick_item")
        agent2 = Agent(node=Node(1, 1), weight=10, state="blocked", goal="reorder")
        agents = [agent1, agent2]

        # Create the deadlock handler
        handler = DeadlockHandler()

        # Test detection
        handler.detect_deadlock(agents)

        # Check if resolution was triggered
        self.assertEqual(len(handler.resolutions), 1, "Should have detected and resolved 1 deadlock")

    def test_deadlock_resolution(self):
        # Create an agent in a blocked state
        agent1 = Agent(node=Node(0, 0), weight=10, state="blocked", goal="pick_item")
        agents = [agent1]

        # Create deadlock handler and detect/resolution
        handler = DeadlockHandler()
        handler.detect_deadlock(agents)
        
        # Check that the agent's position changed (resolution took place)
        self.assertEqual(agent1.node.x, -1, "Agent should have moved back by 1 step in x direction")
        self.assertEqual(agent1.node.y, -1, "Agent should have moved back by 1 step in y direction")
        self.assertEqual(agent1.state, "moving", "Agent state should be 'moving' after deadlock resolution")

if __name__ == "__main__":
    unittest.main()
