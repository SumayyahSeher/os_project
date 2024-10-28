import process_info



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

    print("+=======+===============+===============+==============+=================+")
    print("| P.ID  |  Arrival Time |   Burst Time  | Waiting Time | Turnaround Time |")
    print("+=======+===============+===============+==============+=================+")
    total_WT=0
    total_TAT=0
    for i in range(len(process_list)):
        
        total_WT+= process_list[i].getWaitTime()
        total_TAT+= process_list[i].getTurnaroundTime()

        print("| P", process_list[i].getProcessID(), "\t|",                 # P.ID
                "    ", process_list[i].getArrivalTime(), " \t| ",            # Arrival Time
                "   ", process_list[i].getBurstTime(), " \t|",              # Burst Time
                "   ", process_list[i].getWaitTime(), " \t| ",       # Turnaround Time
                "      ", process_list[i].getTurnaroundTime(), " \t  |", end="")  # Waiting Time 
        print()
    print("+=======+===============+===============+=================+===============+")
    # calculating average WT and TAT
    avg_WT=total_WT/len(process_list)      
    avg_TAT=total_TAT/len(process_list)

    print(f'\n Average Waiting Time:  {avg_WT}')
    print(f' Average Turnaround Time:  {avg_TAT}')
    print("+=======+===============+===============+=================+===============+")
    print("")


def display_gantt_chart_FCFS(process_list):  
    process_list.sort(key=lambda process: process.getArrivalTime())  
    print("===================GANTT CHART======================")

    for k in range(0, len(process_list)):
        print(f"|  P{process_list[k].getProcessID()}  ", end="\t")
    print("| ")


    for i in range(len(process_list)):
        print(process_list[i].getStartingTime() , end="\t") #gantt chart values will be start time fo each process

    print( process_list[-1].getCompletionTime(), end="\t") #last value is end time of last process

    print("")
    

def display_menu():
    # print("\nChoose a CPU Scheduling Algorithm:")
    print("1. First Come First Serve (FCFS)")
    print("2. Shortest Job First")
    # print("2.1. Non-Preemptive Shortest Job First")
    # print("2.2. Preemptive Shortest Job First")
    print("3. Round Robin")
    print("4. Exit")


def main():
    process_list = get_process_list()

    while True:
        print("\nChoose a CPU scheduling algorithm")
        display_menu()
        choice = input()

        if choice == "1":
            print("\n+==================+ First Come First Serve (FCFS) +==================+")
            process_list_FCFS = FCFS(process_list)  # FCFS scheduling
            display_process_data_FCFS(process_list_FCFS)
            display_gantt_chart_FCFS(process_list_FCFS)

        elif choice == "2":
            # sjf_non_preemptive(process_list)  # Non-Preemptive SJF

            print("2.1. Non-Preemptive Shortest Job First")
            print("2.2. Preemptive Shortest Job First")

            choice = input()

            if choice == "2.1":
                # sjf_non_preemptive(process_list)  # Non-Preemptive SJF
                break

            elif choice == "2.2":
                break

        elif choice == "3":
            time_quantum = int(input("Enter Time Quantum for Round Robin: "))
            # round_robin(process_list, time_quantum)  # Round Robin
            break

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

    
    

if __name__ == '__main__':
    main()



