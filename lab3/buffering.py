import threading
import time

# Configuration: Buffer size as per lab manual (e.g., 100 characters)
BUFFER_SIZE = 10 
buffer_a = [None] * BUFFER_SIZE
buffer_b = [None] * BUFFER_SIZE

# Synchronization tools
buffer_lock = threading.Lock()
data_ready = threading.Event() # Signals consumer that a buffer is full
stop_program = False

# Shared state
active_buffer = 'A'
buffer_to_process = None

def fill_buffer():
    """Producer Thread: Reads user input and fills the active buffer[cite: 149]."""
    global active_buffer, buffer_to_process, stop_program
    
    print("Producer: Ready. Type your source code (type 'q' to exit).")
    
    while not stop_program:
        user_input = input(">> ")
        if user_input.lower() == 'q':
            stop_program = True
            data_ready.set() # Wake up consumer to exit
            break

        # Process input character by character into buffers [cite: 150]
        current_idx = 0
        for char in user_input:
            target = buffer_a if active_buffer == 'A' else buffer_b
            target[current_idx] = char
            current_idx += 1

            # Switch buffer if current one is full [cite: 133]
            if current_idx == BUFFER_SIZE:
                with buffer_lock:
                    buffer_to_process = 'A' if active_buffer == 'A' else 'B'
                    active_buffer = 'B' if active_buffer == 'A' else 'A'
                
                print(f"\n[System] Buffer {buffer_to_process} full. Switching to {active_buffer}...")
                data_ready.set() # Notify consumer [cite: 151]
                current_idx = 0
                time.sleep(0.1) # Small delay to allow context switch

def process_data():
    """Consumer Thread: Processes data from the inactive buffer[cite: 152]."""
    global buffer_to_process
    
    while not stop_program:
        data_ready.wait() # Wait until producer signals [cite: 153]
        if stop_program: break
        
        with buffer_lock:
            target = buffer_a if buffer_to_process == 'A' else buffer_b
            print(f"Consumer: Processing Buffer {buffer_to_process}: ", end="")
            
            # Identify 'words' from the buffer [cite: 145]
            content = "".join([c for c in target if c is not None])
            words = content.split()
            print(f"Words found: {words}")
            
            # Clear the buffer for reuse
            if buffer_to_process == 'A':
                buffer_a[:] = [None] * BUFFER_SIZE
            else:
                buffer_b[:] = [None] * BUFFER_SIZE
                
            buffer_to_process = None
            data_ready.clear()

# --- Main Execution ---
if __name__ == "__main__":
    producer = threading.Thread(target=fill_buffer)
    consumer = threading.Thread(target=process_data)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
    print("Program exited gracefully.")