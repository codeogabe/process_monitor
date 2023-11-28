from multiprocessing import process
import psutil as ps
import time
from subprocess import call

def get_file_process(file): #Find file process
    for process in ps.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == 'python3' and file in process.info['cmdline']:
            return process
    return None

def get_process_info(process): #Use file process to get info
    cpu_percent = process.cpu_percent(interval = 1)/ps.cpu_count()
    memory_info = process.memory_info()
    return f"CPU: {cpu_percent:.2f}% | Mem: {memory_info.rss / (1024 * 1024):.2f} MB | "

def format_file_info(file): #Format process info
    return f"{get_process_info(get_file_process(file))}{file}"

def get_system_usage():               
    mem_usage = ps.virtual_memory()
    disk_usage = ps.disk_usage("/").percent
    cpu_usage = ps.cpu_percent(interval=1)
    return f"CPU: {cpu_usage:.2f}% | Mem: {mem_usage.used / (1024 ** 3):.2f} GB | Disk: {disk_usage}%"


def main():
    while True:
        #Files to track
        file_1 = 'todo.py'
        file_2 = 'task_manager.py'

        #Formatted file info
        results_1 = format_file_info(file_1)
        results_2 = format_file_info(file_2)

        #Formatted system info
        system_usage = get_system_usage()

        #Clear terminal
        call('clear')

        #Print everything
        print("--------------FILE USAGE--------------")
        print(results_1)
        print(results_2)
        print("-------------TOTAL USAGE--------------")
        print(system_usage)

        time.sleep(1)

if __name__ == "__main__":
    main()