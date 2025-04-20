import time

class TickSystem:
    def __init__(self, ticks_per_second=4):
        self.ticks_per_second = ticks_per_second  # Number of ticks per second
        self.tick_duration = 1.0 / self.ticks_per_second
        self.last_tick_time = time.time()  # Track the time of the last tick
        self.tick_delay = 0  # Track accumulated delay for catching up

    def get_current_tick(self):
        """Return the current tick count (roughly)"""
        return int(time.time() / self.tick_duration)

    def sync_ticks(self):
        """Ensure the tick system catches up with any delays"""
        current_time = time.time()
        elapsed_time = current_time - self.last_tick_time
        self.tick_delay += elapsed_time

        # If we have missed any ticks, catch up by advancing them
        missed_ticks = int(self.tick_delay // self.tick_duration)
        self.tick_delay %= self.tick_duration

        self.last_tick_time = current_time

        return missed_ticks

    def wait_for_next_tick(self):
        """Wait for the next tick time to ensure the tick rate is maintained"""
        current_time = time.time()
        next_tick_time = self.last_tick_time + self.tick_duration
        sleep_time = max(0, next_tick_time - current_time)
        time.sleep(sleep_time)
        self.last_tick_time = time.time()  # Update last_tick_time after sleeping
