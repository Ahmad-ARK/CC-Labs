# 2022-CS-31

import threading
import time

BUFFER_SIZE = 100
buffer_a = [None] * BUFFER_SIZE
buffer_b = [None] * BUFFER_SIZE

buffer_lock = threading.Lock()
data_ready = threading.Event() 
stop_program = False

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
            data_ready.set() 
            break

        current_idx = 0
        for char in user_input:
            target = buffer_a if active_buffer == 'A' else buffer_b
            target[current_idx] = char
            current_idx += 1

            if current_idx == BUFFER_SIZE:
                with buffer_lock:
                    buffer_to_process = 'A' if active_buffer == 'A' else 'B'
                    active_buffer = 'B' if active_buffer == 'A' else 'A'
                
                print(f"\n[System] Buffer {buffer_to_process} full. Switching to {active_buffer}...")
                data_ready.set() 
                current_idx = 0
                time.sleep(0.1) 

def process_data():
    """Consumer Thread: Processes data from the inactive buffer[cite: 152]."""
    global buffer_to_process
    
    while not stop_program:
        data_ready.wait() 
        if stop_program: break
        
        with buffer_lock:
            target = buffer_a if buffer_to_process == 'A' else buffer_b
            print(f"Consumer: Processing Buffer {buffer_to_process}: ", end="")
            
            content = "".join([c for c in target if c is not None])
            words = content.split()
            print(f"Words found: {words}")
            
            if buffer_to_process == 'A':
                buffer_a[:] = [None] * BUFFER_SIZE
            else:
                buffer_b[:] = [None] * BUFFER_SIZE
                
            buffer_to_process = None
            data_ready.clear()

if __name__ == "__main__":
    producer = threading.Thread(target=fill_buffer)
    consumer = threading.Thread(target=process_data)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
    print("Program exited gracefully.")