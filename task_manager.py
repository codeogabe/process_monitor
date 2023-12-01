
from os import pread
import psutil as ps
import time
from subprocess import call

#For highlighting text
class colors:
    RESET = "\033[0m"
    RED = "\033[91m"

#Find file process
def get_file_process(file_list): 
    process_list = []

    #Finds all processes of filename
    for file in file_list:
        for process in ps.process_iter(['pid', 'name', 'cmdline']):
            if process.info['name'] == 'python3' and file in process.info['cmdline']:
                if process not in process_list:
                    process_list.append(process)
                    process
    return process_list

#Get file usage
def get_file_usage(file_list): 
    print = ""
    process_list = get_file_process(file_list) 

    for process in process_list:   
        cpu_percent = process.cpu_percent(interval = .3) #Dividing by total cores gives average use
        memory_info = process.memory_info()
        print += f"CPU: {cpu_percent:.2f}% | Mem: {memory_info.rss / (1024 * 1024):.2f} MB | PID: {process.info['pid']} |\n"
    return print

#Get system usage
def get_system_usage():
    with ps.Process().oneshot():               
        mem_usage = ps.virtual_memory()
        disk_usage = ps.disk_usage("/").percent
        cpu_usage = ps.cpu_percent(interval=.3)
    return f"CPU: {cpu_usage:.2f}% | Mem: {mem_usage.used / (1024 ** 3):.2f} GB | Disk: {disk_usage}% |"

#Get file core usage
def get_file_cores(file_list):
    result = ""
    process_core_list = list()
    process_list = get_file_process(file_list)

    

    cpu_percentages = ps.cpu_percent(percpu=True, interval=.3)
    for process in process_list:
        process_core_list.append(process.cpu_num())

    #Highlights the core used by file
    for i in range(len(cpu_percentages)):
        for process in process_core_list:
            if process == i:
                result += f"{colors.RED}Core {i+1:2}: {cpu_percentages[i]:4}%{colors.RESET}|"
            else:
                result += f"Core {i+1:2}: {cpu_percentages[i]:4}%|"
        result += "\n"
    return result

def main():
    while True:
        #Append files to track
        file_list = []
        file_list.append('todo.py')


        with ps.Process().oneshot():

            #File cpu/mem usage
            results = get_file_usage(file_list)

            #File core usage
            results_cores = get_file_cores(file_list)

            #System usage
            system_usage = get_system_usage()

        #Clear terminal
        call('clear')

        #Print everything
        print("--------------FILE USAGE--------------")
        print(results)
        print("-------------TOTAL USAGE--------------")
        print(system_usage)
        print("--------------CPU CORES---------------")
        print(results_cores)


if __name__ == "__main__":
    main()