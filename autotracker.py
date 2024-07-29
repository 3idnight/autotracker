import time
import win32gui
import win32process
import psutil
import logging

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

if __name__ == "__main__":
    logging.basicConfig(filename='application_usage.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    active_window = None
    active_start_time = None

    while True:
        current_window_title, current_process_name = get_active_window()

        if current_window_title != active_window:
            if active_window is not None:
                duration = time.time() - active_start_time
                logging.info(f"Window: {active_window} (Process: {active_process_name}) - Duration: {duration:.2f} seconds")

            active_window = current_window_title
            active_process_name = current_process_name
            active_start_time = time.time()

        time.sleep(1)