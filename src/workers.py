import threading
import time
from typing import List, Any, Optional
from src.buffer import CustomBoundedBuffer

# Sentinel value to signal termination
SENTINEL = None

class Producer(threading.Thread):
    def __init__(self, source: List[Any], buffer: CustomBoundedBuffer):
        super().__init__(name="Producer")
        self.source = source
        self.buffer = buffer

    def run(self):
        print(f"[{self.name}] Started.")
        try:
            for item in self.source:
                # Simulate processing
                time.sleep(0.01)
                self.buffer.put(item)
                print(f"[{self.name}] Produced: {item}")
        finally:
            # Ensure shutdown signal is sent
            self.buffer.put(SENTINEL)
            print(f"[{self.name}] Finished.")

class Consumer(threading.Thread):
    def __init__(self, buffer: CustomBoundedBuffer, destination: List[Any]):
        super().__init__(name="Consumer")
        self.buffer = buffer
        self.destination = destination

    def run(self):
        print(f"[{self.name}] Started.")
        while True:
            item = self.buffer.get()
            if item is SENTINEL:
                # Propagate signal if needed
                self.buffer.put(SENTINEL)
                break
            # Simulate processing
            time.sleep(0.02)
            self.destination.append(item)
            print(f"[{self.name}] Consumed: {item}")
        print(f"[{self.name}] Finished.")