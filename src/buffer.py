import threading
from typing import List, Any

class CustomBoundedBuffer:
    """
    A thread-safe, bounded buffer implementing the Wait/Notify mechanism.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer: List[Any] = []
        
        # Internal Lock for mutual exclusion
        self._lock = threading.RLock()
        
        # Condition variables for Wait/Notify
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item: Any) -> None:
        """Adds item to buffer. Blocks if full."""
        with self._lock:
            while len(self.buffer) >= self.capacity:
                self._not_full.wait()
            
            self.buffer.append(item)
            self._not_empty.notify()

    def get(self) -> Any:
        """Removes item from buffer. Blocks if empty."""
        with self._lock:
            while not self.buffer:
                self._not_empty.wait()
            
            item = self.buffer.pop(0)
            self._not_full.notify()
            return item