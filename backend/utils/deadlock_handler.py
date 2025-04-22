class DeadlockHandler:
    def __init__(self):
        self.resolutions = []

    def detect_deadlock(self, agents):
        """
        Detects if there is any deadlock scenario.
        Assumes that agents can be in blocked state and not able to progress.
        """
        blocked_agents = [agent for agent in agents if agent.state == "blocked"]

        # Deadlock detection: If there is at least one agent in a blocked state, resolve it.
        if len(blocked_agents) >= 1:
            self.resolve_deadlock(blocked_agents)

    def resolve_deadlock(self, agents):
        """
        Resolves deadlock by reversing the last move of one of the blocked agents.
        This is a simple resolution, could be more complex based on needs.
        """
        # For simplicity, we can move one of the agents back a step (could be improved with actual path data)
        for agent in agents:
            if agent.state == "blocked":
                self.resolutions.append(f"Resolving deadlock by moving {agent} back.")
                agent.node.x -= 1  # Move back by 1 step in x direction
                agent.node.y -= 1  # Move back by 1 step in y direction
                agent.state = "moving"  # Change state to 'moving'
                break  # Resolve only one agent for simplicity
