import requests
import time

# Base URL of the Flask application
base_url = 'http://127.0.0.1:5000'

# Function to update exam details
def update_exam_details(start_time, end_time, leave_time, num_students):
    url = f"{base_url}/"
    data = {
        'start_time': start_time,
        'end_time': end_time,
        'leave_time': leave_time,
        'num_students': num_students
    }
    response = requests.post(url, data=data)
    return response

# Function to add a note
def add_note(note):
    url = f"{base_url}/add_note"
    data = {
        'note': note
    }
    response = requests.post(url, data=data)
    return response

# Function to simulate stopwatch functionality
def simulate_stopwatch():
    # Start timer
    start_time = time.strftime("%H:%M", time.localtime(time.time() + 10))  # Start in 10 seconds
    update_exam_details(start_time, '12:00', '10:30', 50)
    time.sleep(12)  # Wait for 12 seconds to start stopwatch
    
    # Check time display and alerts
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"Current Time: {current_time}")
    response = requests.get(base_url)
    print(f"Current HTML Content:\n{response.text}")
    
    # Add a note
    add_note("Testing note addition")
    
    # Stop timer
    time.sleep(5)
    response = requests.get(base_url)
    print(f"Updated HTML Content:\n{response.text}")

if __name__ == "__main__":
    simulate_stopwatch()
