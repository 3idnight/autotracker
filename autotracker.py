import time
import win32gui
import win32process
import psutil
import logging
from collections import defaultdict

def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        process_name = process.name()
        return window_title, process_name
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        logging.warning(f"Error retrieving process info: {e}")
        return None, None

def update_log_file(window_durations):
    with open('application_usage.log', 'w', encoding='utf-8') as log_file:
        for (window, process), duration in window_durations.items():
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Window: {window} (Process: {process}) - Duration: {duration:.2f} seconds\n")

if __name__ == "__main__":
    logging.basicConfig(filename='application_usage.log', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')
    
    active_window = None
    active_start_time = None
    window_durations = defaultdict(float)

    while True:
        current_window_title, current_process_name = get_active_window()

        if current_window_title and current_process_name:
            if current_window_title != active_window:
                if active_window is not None:
                    duration = time.time() - active_start_time
                    window_durations[(active_window, active_process_name)] += duration

                    # Update the log file with the latest durations
                    update_log_file(window_durations)

                active_window = current_window_title
                active_process_name = current_process_name
                active_start_time = time.time()

        time.sleep(1)
