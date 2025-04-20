# tests/test_tick_system.py

import unittest
from utils.tick_system import TickSystem

class TestTickSystem(unittest.TestCase):
    def test_sync_ticks(self):
        tick_system = TickSystem(ticks_per_second=4)

        # Simulate 1 second passing
        tick_system.last_tick_time -= 1

        missed_ticks = tick_system.sync_ticks()
        self.assertEqual(missed_ticks, 4, "Missed ticks should be 4 after 1 second")

    def test_wait_for_next_tick(self):
        tick_system = TickSystem(ticks_per_second=4)

        # Store the current tick time
        previous_time = tick_system.last_tick_time

        # Wait for next tick (this will just simulate the tick rate behavior)
        tick_system.wait_for_next_tick()
        self.assertGreater(tick_system.last_tick_time, previous_time, "Tick time should have advanced")

if __name__ == "__main__":
    unittest.main()
