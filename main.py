from src.buffer import CustomBoundedBuffer
from src.workers import Producer, Consumer

def main():
    print("--- Starting Assignment 1: Producer-Consumer ---")
    
    # 1. Setup Data and Resources
    source_data = list(range(1, 21))
    destination_data = []
    shared_buffer = CustomBoundedBuffer(capacity=5)
    
    # 2. Initialize Threads
    producer = Producer(source_data, shared_buffer)
    consumer = Consumer(shared_buffer, destination_data)
    
    # 3. Start Execution
    producer.start()
    consumer.start()
    
    # 4. Wait for Completion
    producer.join()
    consumer.join()
    
    # 5. Verify Result
    print("\n--- Processing Complete ---")
    print(f"Source Items: {len(source_data)}")
    print(f"Consumed Items: {len(destination_data)}")
    
    if source_data == destination_data:
        print("SUCCESS: Data integrity maintained.")
    else:
        print("FAILURE: Data mismatch.")

if __name__ == "__main__":
    main()