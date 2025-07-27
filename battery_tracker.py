import socket
import re
import datetime

HOST = 'localhost'  # Cooja's Serial Socket Server host
PORT = 60001        # Default port

def extract_battery(message):
    match = re.search(r'Battery:\s*(\d+)%', message)
    return int(match.group(1)) if match else None

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("Connected! Tracking battery levels...\n")

        with open("battery_log.txt", "a") as log_file:
            while True:
                data = s.recv(1024).decode('utf-8').strip()
                if data:
                    battery_level = extract_battery(data)
                    if battery_level is not None:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_entry = f"[{timestamp}] Battery: {battery_level}%"
                        print(log_entry)
                        log_file.write(log_entry + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTracking stopped by user.")
