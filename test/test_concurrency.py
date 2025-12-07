import unittest
import time
import threading

from src.buffer import CustomBoundedBuffer
from src.workers import Producer, Consumer, SENTINEL

class TestProducerConsumer(unittest.TestCase):
    
    # Helper to print test status clearly at the start of each test
    def setUp(self):
        print(f"\n--- Running Test: {self._testMethodName} ---")

    def test_1_data_integrity_and_deadlock_free(self):
        """1. Verifies complete data transfer, order integrity, and graceful shutdown (Core Test)."""
        # Larger dataset for better concurrency stress
        source = list(range(1, 200))
        dest = []
        # Small capacity (3) forces frequent blocking and signaling
        buf = CustomBoundedBuffer(capacity=3) 
        
        p = Producer(source, buf)
        c = Consumer(buf, dest)
        
        start_time = time.time()
        p.start()
        c.start()
        
        # Use join with a timeout to verify no deadlock occurs (Liveness check)
        p.join(timeout=5) 
        c.join(timeout=5)
        end_time = time.time()
        
        # Assertions for Thread Synchronization, Concurrent Programming, and Integrity
        self.assertFalse(p.is_alive(), "Producer failed to terminate (Possible Deadlock/Bug)")
        self.assertFalse(c.is_alive(), "Consumer failed to terminate (Possible Deadlock/Bug)")
        self.assertEqual(source, dest, "Data transferred does not match source or order.")
        print(f"Test 1 Passed (Time: {end_time - start_time:.2f}s): Full transfer and integrity verified.")

    def test_2_consumer_blocking_on_empty(self):
        """2. Verifies Consumer's Wait/Notify mechanism on an empty buffer (Testing .get() blocking)."""
        buf = CustomBoundedBuffer(capacity=1)
        
        # Task that will block immediately
        def consumer_task():
            buf.get()
            
        t = threading.Thread(target=consumer_task, name="BlockingConsumer")
        t.start()
        
        # Give the consumer a moment to acquire the lock and block
        time.sleep(0.1) 
        
        # ASSERTION 1: Consumer should be alive (blocked)
        self.assertTrue(t.is_alive(), "Consumer should be blocked, waiting for data (Wait/Notify failure).")
        
        # Unblock it by putting an item
        buf.put(99)
        t.join(timeout=1)
        
        # ASSERTION 2: Consumer should finish shortly after being notified
        self.assertFalse(t.is_alive(), "Consumer failed to finish after being unblocked.")
        print("Test 2 Passed: Consumer blocking/unblocking verified.")
        
    def test_3_producer_blocking_on_full(self):
        """3. Verifies Producer's blocking mechanism on a full buffer (Testing .put() blocking)."""
        buf = CustomBoundedBuffer(capacity=1) # Very small buffer
        buf.put(1) # Fill the buffer
        
        # Task that attempts to put the second item, which should block
        def producer_task():
            buf.put(2)
            
        t = threading.Thread(target=producer_task, name="BlockingProducer")
        t.start()
        
        # Give the producer a moment to acquire the lock and block
        time.sleep(0.1) 
        
        # ASSERTION 1: Producer should be alive (blocked)
        self.assertTrue(t.is_alive(), "Producer should be blocked, waiting for space (Blocking Queue failure).")
        
        # Unblock it by getting an item
        buf.get() 
        t.join(timeout=1)
        
        # ASSERTION 2: Producer should finish shortly after being notified
        self.assertFalse(t.is_alive(), "Producer failed to finish after being unblocked.")
        print("Test 3 Passed: Producer blocking/unblocking verified.")
        
    def test_4_graceful_shutdown_on_empty_source(self):
        """4. Verifies the system handles the edge case of an empty source list cleanly."""
        source = []
        dest = []
        buf = CustomBoundedBuffer(capacity=5)
        
        p = Producer(source, buf)
        c = Consumer(buf, dest)
        
        p.start()
        c.start()
        p.join(timeout=1)
        c.join(timeout=1)
        
        # Assertions
        self.assertFalse(p.is_alive(), "Empty Producer failed to terminate.")
        self.assertFalse(c.is_alive(), "Consumer failed to terminate after empty source.")
        self.assertEqual(dest, [], "Destination should be empty.")
        print("Test 4 Passed: Graceful shutdown on empty source verified.")
        
    def test_5_multiple_consumers_and_load_balancing(self):
        """5. Verifies that multiple consumers can concurrently drain the queue and terminate gracefully."""
        source = list(range(1, 41)) # 40 items
        dest_1 = []
        dest_2 = []
        
        buf = CustomBoundedBuffer(capacity=5) 
        
        p = Producer(source, buf)
        c1 = Consumer(buf, dest_1)
        c2 = Consumer(buf, dest_2)
        
        p.start()
        c1.start()
        c2.start()
        
        # Wait for completion
        p.join(timeout=5)
        c1.join(timeout=5)
        c2.join(timeout=5)
        
        # Assertions for Multi-Thread Synchronization
        self.assertFalse(c1.is_alive())
        self.assertFalse(c2.is_alive())
        
        # Combine and sort the output to verify all data was transferred (order is not preserved across consumers)
        final_destination = sorted(dest_1 + dest_2)
        
        self.assertEqual(source, final_destination, "Data mismatch in multi-consumer test.")
        
        # Verify load balancing (ensures both threads actually consumed data)
        self.assertTrue(len(dest_1) > 0 and len(dest_2) > 0, "One consumer was starved (did not receive data).")
        print("Test 5 Passed: Multi-consumer concurrency and load balancing verified.")
        
    def test_6_generic_data_types_and_min_capacity(self):
        """6. Verifies system handles non-primitive data types and minimum capacity (1)."""
        # Source data includes strings, integers, and a dictionary (complex types)
        source = ["apple", {"id": 101, "price": 5.99}, "banana", 42] 
        dest = []
        
        # Test with capacity=1 (the smallest possible size) to maximize contention
        buf = CustomBoundedBuffer(capacity=1) 
        
        p = Producer(source, buf)
        c = Consumer(buf, dest)
        
        p.start()
        c.start()
        
        p.join(timeout=5)
        c.join(timeout=5)
        
        # Assertions
        self.assertFalse(p.is_alive())
        self.assertFalse(c.is_alive())
        
        # Verify the content and sequence
        self.assertEqual(source, dest, "Data types were corrupted or sequence was broken.")
        print("Test 6 Passed: Generic data types and min capacity verified.")


if __name__ == '__main__':
    # Running unittest.main() provides the required clear pass/fail status summary
    unittest.main()