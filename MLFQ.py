import matplotlib.pyplot as plt
#this class stores information about each process
class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.completion = 0
        self.response = -1
        self.waiting = 0
        self.turnaround = 0
        self.remaining_burst = burst    
#reset process valuses when algorithm is change
    def reset(self):
        self.completion = 0
        self.response = -1
        self.waiting = 0
        self.turnaround = 0
        self.remaining_burst = self.burst
#sorts processes based on arrival time and each process is executed in order.
def fcfs(queue):
    queue.sort(key=lambda p: p.arrival)
    current_time = 0
    for process in queue:
        if current_time < process.arrival:
            current_time = process.arrival
        if process.response == -1:
            process.response = current_time - process.arrival
        process.completion = current_time + process.burst
        process.turnaround = process.completion - process.arrival
        process.waiting = process.turnaround - process.burst
        current_time = process.completion
#Processes are sorted by arrival time in reverse order.The process that arrived later is executed first.
def lcfs(queue):
    queue.sort(key=lambda p: (-p.arrival, p.pid))
    current_time = 0
    for process in queue:
        if current_time < process.arrival:
            current_time = process.arrival
        if process.response == -1:
            process.response = current_time - process.arrival
        process.completion = current_time + process.burst
        process.turnaround = process.completion - process.arrival
        process.waiting = process.turnaround - process.burst
        current_time = process.completion
#Processes are first sorted by arrival time and then by priority.
def priority_scheduling(queue):
    queue.sort(key=lambda p: (p.arrival, p.priority))
    current_time = 0
    for process in queue:
        if current_time < process.arrival:
            current_time = process.arrival
        if process.response == -1:
            process.response = current_time - process.arrival
        process.completion = current_time + process.burst
        process.turnaround = process.completion - process.arrival
        process.waiting = process.turnaround - process.burst
        current_time = process.completion
#Processes are executed in round-robin fashion until remaining_burst becomes zero.
def round_robin(queue, quantum):
    current_time = 0
    ready_queue = []
    queue.sort(key=lambda p: p.arrival)
    remaining_processes = queue[:]
    gantt_log = []  
    
    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0].arrival <= current_time:
            ready_queue.append(remaining_processes.pop(0))
        if ready_queue:
            process = ready_queue.pop(0)
            if process.response == -1:
                process.response = current_time - process.arrival
            execution_time = min(process.remaining_burst, quantum)
            start_time = current_time
            current_time += execution_time
            process.remaining_burst -= execution_time
            end_time = current_time
            gantt_log.append((process.pid, start_time, end_time))  
            
            if process.remaining_burst == 0:
                process.completion = current_time
                process.turnaround = process.completion - process.arrival
                process.waiting = process.turnaround - process.burst
            else:
                ready_queue.append(process)
        else:
            current_time += 1

    return gantt_log  


def plot_gantt_chart(log, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 3))
    for entry in log:
        process_id, start_time, end_time = entry
        ax.barh(1, end_time - start_time, left=start_time, edgecolor='black', label=f"P{process_id}")
        ax.text((start_time + end_time) / 2, 1, f"P{process_id}", ha='center', va='center', color='white', fontsize=10)
    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(f"Gantt Chart - {algorithm_name}")
    plt.show()

def display_gantt_chart_rr(processes, log):
    plot_gantt_chart(log, "Round Robin")

def display_gantt_chart(processes, algorithm_name):
    log = []
    current_time = 0

    for p in processes:
        start_time = max(current_time, p.arrival)
        end_time = start_time + p.burst
        log.append((p.pid, start_time, end_time))
        current_time = end_time

    plot_gantt_chart(log, algorithm_name)


def get_process_input():
    n = int(input("Enter the number of processes: "))
    processes = []
    for i in range(n):
        pid = i + 1
        arrival = int(input(f"Enter arrival time for process {pid}: "))
        burst = int(input(f"Enter burst time for process {pid}: "))
        priority = int(input(f"Enter priority for process {pid}: "))
        processes.append(Process(pid, arrival, burst, priority))
    return processes


def print_table(processes):
    print("\nP\treq\tService\tResponse\tWait\tRec")
    for p in processes:
        print(f"P{p.pid}\t{p.arrival}\t{p.burst}\t{p.response}\t\t{p.waiting}\t{p.turnaround}")


def main():
    processes = get_process_input()
    
    print("\nSelect the algorithm you want (separate with comma):")
    print("1. FCFS\n2. LCFS\n3. Priority Scheduling\n4. Round Robin")
    choices = input("Select (in priority order): ").split(',')
    choices = [int(c.strip()) for c in choices]
    
    quantum = None
    if 4 in choices:
        quantum = int(input("Enter Quantum: "))
    
    for choice in choices:
        for p in processes:
            p.reset()
        
        print(f"\nImplementation of algorithm number {choice}...")
        if choice == 1:
            fcfs(processes)
            print_table(processes)
            display_gantt_chart(processes, "FCFS")
        elif choice == 2:
            lcfs(processes)
            print_table(processes)
            display_gantt_chart(processes, "LCFS")
        elif choice == 3:
            priority_scheduling(processes)
            print_table(processes)
            display_gantt_chart(processes, "Priority Scheduling")
        elif choice == 4 and quantum:
            gantt_log = round_robin(processes, quantum)
            print_table(processes)
            display_gantt_chart_rr(processes, gantt_log)
        else:
            print(f"Algorithm number {choice} NOT VALID!")
            continue


main()
