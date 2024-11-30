import process_info
import bankers
import LRU
import OptimalAlgorithm

def get_process_list():
    process_list = []
    n = int(input("Enter the number of processes: "))

    for i in range(1, n+1):
        process_id = i
        print("+------------------------------+")
        arrival_time = int(input(f"P[{process_id}] Arrival time: "))
        burst_time = int(input(f"P[{process_id}] Busrt time: "))

        process= process_info.Process(process_id,arrival_time,burst_time)

        process_list.append(process)

    return process_list

def FCFS(process_list):
    # sort based on arrival time
    process_list.sort(key=lambda process: process.getArrivalTime()) 

    #start & end time for1st process
    process_list[0].setStartingTime(0) #P! start time=0
    process_list[0].setCompletionTime(process_list[0].getStartingTime() + process_list[0].getBurstTime())

    for i in range(1, len(process_list)):
        if process_list[i-1].getCompletionTime() > process_list[i].getArrivalTime(): # if previous process still executing when new arrives
            process_list[i].setStartingTime(process_list[i-1].getCompletionTime()) #no preemption so needs to wait for previous process to complete
        else:
            process_list[i].setStartingTime(process_list[i].getArrivalTime()) #no need to wait

        # completion time= start time+burst time    
        process_list[i].setCompletionTime(process_list[i].getStartingTime() + process_list[i].getBurstTime())

    # calculating waiting time and turn around time
    for i in range(len(process_list)):
        process_list[i].wait_time=process_list[i].getStartingTime()-process_list[i].getArrivalTime() #WT= start time-arrival
        process_list[i].TAT= process_list[i].getCompletionTime()-process_list[i].getArrivalTime() #TAT= end time-arrival

    return process_list    

    
def display_process_data_FCFS(process_list):
    process_list.sort(key=lambda process: process.getProcessID())

    print("+==========+===================+===================+===================+=====================+")
    print("| Process  |  Arrival Time(ms) |   Burst Time(ms)  | Waiting Time(ms)  | Turnaround Time(ms) |")
    print("+==========+===================+===================+===================+=====================+")
    total_WT=0
    total_TAT=0
    for i in range(len(process_list)):
        
        total_WT+= process_list[i].getWaitTime()
        total_TAT+= process_list[i].getTurnaroundTime()

        print("| P{:<8}| {:^18}| {:^18}| {:^18}| {:^21}|".format(
        process_list[i].getProcessID(),
        process_list[i].getArrivalTime(),
        process_list[i].getBurstTime(),
        process_list[i].getWaitTime(),
        process_list[i].getTurnaroundTime()
        ))
    print("+==========+===================+===================+===================+=====================+")
    # calculating average WT and TAT
    avg_WT=total_WT/len(process_list)      
    avg_TAT=total_TAT/len(process_list)

    print(f'\n Average Waiting Time:  {avg_WT} ms')
    print(f' Average Turnaround Time:  {avg_TAT} ms')
    print("+=======+===============+===============+=================+===============+")
    print("")

def display_gantt_chart_FCFS(process_list):  
    process_list.sort(key=lambda process: process.getArrivalTime())  
    print("===================GANTT CHART (FCFS)======================")

    for k in range(0, len(process_list)):
        print(f"|  P{process_list[k].getProcessID()}  ", end="\t")
    print("| ")

    for i in range(len(process_list)):
        print(process_list[i].getStartingTime() , end="\t") #gantt chart values will be start time fo each process

    print( process_list[-1].getCompletionTime(), end="\t") #last value is end time of last process
    print("")

#SJF- NON-PREEMPTIVE
def non_preemptive(process_list):
    process_list.sort(key=lambda process: (process.getArrivalTime(), process.getBurstTime()))
    completed_processes = []
    current_time = 0

    while len(completed_processes) < len(process_list):
        ready_queue = [p for p in process_list if p.getArrivalTime() <= current_time and p not in completed_processes]
        if ready_queue:
            process_to_execute = min(ready_queue, key=lambda x: x.getBurstTime())
            process_to_execute.setStartingTime(current_time)
            current_time += process_to_execute.getBurstTime()
            process_to_execute.setCompletionTime(current_time)
            process_to_execute.wait_time = process_to_execute.getStartingTime() - process_to_execute.getArrivalTime()
            process_to_execute.TAT = process_to_execute.getCompletionTime() - process_to_execute.getArrivalTime()
            completed_processes.append(process_to_execute)
        else:
            current_time += 1

    return completed_processes

def display_process_data_non_preemptive(process_list):
    process_list.sort(key=lambda process: process.getProcessID())

    print("+==========+===================+===================+===================+=====================+")
    print("| Process  |  Arrival Time(ms) |   Burst Time(ms)  | Waiting Time(ms)  | Turnaround Time(ms) |")
    print("+==========+===================+===================+===================+=====================+")
    total_WT = 0
    total_TAT = 0
    for i in range(len(process_list)):
        total_WT += process_list[i].getWaitTime()
        total_TAT += process_list[i].getTurnaroundTime()
        print("| P{:<8}| {:^18}| {:^18}| {:^18}| {:^21}|".format(
        process_list[i].getProcessID(),
        process_list[i].getArrivalTime(),
        process_list[i].getBurstTime(),
        process_list[i].getWaitTime(),
        process_list[i].getTurnaroundTime()
        ))
    print("+==========+===================+===================+===================+=====================+")
    avg_WT = total_WT / len(process_list)
    avg_TAT = total_TAT / len(process_list)
    print(f'\n Average Waiting Time:  {avg_WT}')
    print(f' Average Turnaround Time:  {avg_TAT}')
    print("+=======+===============+===============+=================+===============+")
    print("")

def display_gantt_chart_non_preemptive(process_list):
    completed_processes = []
    current_time = 0
    gantt_chart = []

    process_list.sort(key=lambda process: process.getArrivalTime())

    while len(completed_processes) < len(process_list):
        ready_queue = [p for p in process_list if p.getArrivalTime() <= current_time and p not in completed_processes]
        
        if ready_queue:
            process_to_execute = min(ready_queue, key=lambda x: x.getBurstTime())
            gantt_chart.append((process_to_execute.getProcessID(), current_time))
            current_time += process_to_execute.getBurstTime()
            process_to_execute.setStartingTime(current_time - process_to_execute.getBurstTime())
            process_to_execute.setCompletionTime(current_time)
            completed_processes.append(process_to_execute)
        else:
            current_time += 1

    gantt_chart.append((None, current_time))

    print("===================GANTT CHART (Non-Preemptive SJF)======================")
    for i in range(len(gantt_chart) - 1):
        pid = gantt_chart[i][0]
        print(f"|  P{pid}  ", end="\t")
    print("| ")

    for time in [start_time for _, start_time in gantt_chart]:
        print(time, end="\t")
    print()

#SJF-PREEMPTIVE
def sjf_preemptive(process_list):
    gantt_chart = []
    time = 0
    ready_queue = []
    completed_processes = []
    original_burst_times = {process.getProcessID(): process.getBurstTime() for process in process_list}
    while len(completed_processes) < len(process_list):
        for process in process_list:
            if process.getArrivalTime() <= time and process not in ready_queue and process not in completed_processes:
                ready_queue.append(process)
        if ready_queue:
            ready_queue.sort(key=lambda p: p.getBurstTime())
            current_process = ready_queue[0]
            if current_process.getStartingTime() is None:
                current_process.setStartingTime(time)
            gantt_chart.append((current_process.getProcessID(), time, time + 1))
            time += 1            
            current_process.setBurstTime(current_process.getBurstTime() - 1)
            if current_process.getBurstTime() == 0:
                current_process.setCompletionTime(time)
                TAT = time - current_process.getArrivalTime()  
                current_process.TAT = TAT
                current_process.wait_time = TAT - original_burst_times[current_process.getProcessID()]  # Waiting Time
                completed_processes.append(current_process)
                ready_queue.remove(current_process)
        else:
            time += 1  
    
    return process_list, gantt_chart
def display_process_data_preemptive(process_list, original_burst_times):
    print("+==========+===================+===================+===================+=====================+")
    print("| Process  |  Arrival Time(ms) |   Burst Time(ms)  | Waiting Time(ms)  | Turnaround Time(ms) |")
    print("+==========+===================+===================+===================+=====================+")
    total_WT = 0
    total_TAT = 0
    for process in process_list:
        total_WT += process.getWaitTime()
        total_TAT += process.getTurnaroundTime()
        print("| P{:<8}| {:^18}| {:^18}| {:^18}| {:^21}|".format(
        process.getProcessID(),
        process.getArrivalTime(),
        process.getBurstTime(),
        process.getWaitTime(),
        process.getTurnaroundTime()
        ))
    print("+==========+===================+===================+===================+=====================+")
    avg_WT = total_WT / len(process_list)
    avg_TAT = total_TAT / len(process_list)
    print(f'\n Average Waiting Time:  {avg_WT}')
    print(f' Average Turnaround Time:  {avg_TAT}')
    print("+==========+===============+===============+==============+=================+")
    print("")


def display_gantt_chart_preemptive(gantt_chart):
    print("\n=================== GANTT CHART (Preemptive SJF) =======================")
    print("Process Execution Timeline:")
    processes = []
    times = []
    for segment in gantt_chart:
        if not processes or processes[-1] != segment[0]: 
            processes.append(segment[0])
            times.append(segment[1])
    for pid in processes:
        print(f"|  P{pid}  ", end="\t")
    print("| ")
    for time in times:
        print(f"{time}\t", end="")
    print(gantt_chart[-1][2])

#MAIN MENU
def display_menu():
    print("1. First Come First Serve (FCFS)")
    print("2. Shortest Job First")
    print("3. Round Robin")
    print("4. Banker's Algorithm")
    print("5. Page Replacement Algorithm")
    print("6. Exit")

def main():
    
    while True:
        print("\nChoose a CPU scheduling algorithm")
        display_menu()
        choice = input()

        if choice == "1":
            process_list = get_process_list()
            print("\n+==================+ First Come First Serve (FCFS) +==================+")
            process_list_FCFS = FCFS(process_list)  # FCFS scheduling
            display_process_data_FCFS(process_list_FCFS)
            display_gantt_chart_FCFS(process_list_FCFS)

        elif choice == "2":
             while True: 
                print("\nChoose Non-Preemptive or Preemptive")
                print("1. Non-Preemptive Shortest Job First")
                print("2. Preemptive Shortest Job First")
                print("3. Back")
                choice1 = input()
                if choice1 == "1":
                    process_list = get_process_list()
                    print("\n+==================+ Non-Preemptive Shortest Job First (SJF) +==================+")
                    process_list_SJF = non_preemptive(process_list)
                    display_process_data_non_preemptive(process_list_SJF)
                    display_gantt_chart_non_preemptive(process_list_SJF)
                     

                elif choice1 == "2":
                   process_list = get_process_list()
                   print("\n+==================+ Preemptive Shortest Job First (SJF) +==================+")
                   original_burst_times = {process.getProcessID(): process.getBurstTime() for process in process_list}
                   process_list_preemptive, gantt_chart = sjf_preemptive(process_list)
                   display_process_data_preemptive(process_list_preemptive, original_burst_times)
                   display_gantt_chart_preemptive(gantt_chart)

                elif choice1 == "3":
                    print("Going back to main menu")  
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            time_quantum = int(input("Enter Time Quantum for Round Robin: "))
            # round_robin(process_list, time_quantum)  # Round Robin
            
        elif choice == "4":
            bankers.banker_main()
            
        elif choice == "5":
            while True: 
                print("\nChoose a Page Replacement Algorithm:")
                print("1. First In First Out (FIFO)")
                print("2. Optimal")
                print("3. Least Recently Used (LRU)")
                print("4. Back")
                choice1 = input("Enter your choice: ")
                if choice1 == "1":
                    print("FIFO Algorithm not implemented yet.") 
                      
                elif choice1 == "2":
                    OptimalAlgorithm.opt_main()
            
                elif choice1 == "3":
                    LRU.lru_main() 
                    
                elif choice1 == "4":
                    print("Going back to main menu")  
                    break
        
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "6":
            print("Exiting program")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
