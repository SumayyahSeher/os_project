class RoundRobin:

    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = []
            process_id = i+1
            arrival_time = int(input(f" P[{process_id}] Arrival Time: "))
            burst_time = int(input(f" P[{process_id}] Burst Time: "))
            print("+=======+===============+===============+=================+===============+")
            print("")
            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])

            #'0' is the state of the process. 0 means not executed and 1 means execution complete

            process_data.append(temporary)

        time_quantum = int(input("Enter Time Quantum: "))
        RoundRobin.schedulingProcess(self, process_data, time_quantum)

    def drawGanttChart(self, process_data, executed_process, start_time, exit_time):
        print("\n===================GANTT CHART (Round Robin)======================")
        for process_id in executed_process:
            print(f"| P{process_id} ", end="")
        print("|")

        for i in range(len(start_time)):
            print(f"{start_time[i]:^{exit_time[i] - start_time[i]}}", end=" ")
        print("\n")

    def schedulingProcess(self, process_data, time_quantum):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])

        #Sort processes according to the Arrival Time

        while 1:
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1

                    #The above if loop checks that the next process is not a part of ready_queue

                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []

                    #The above if loop adds a process to the ready_queue only if it is not already present in it

                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))

                    #The above if loop makes sure that the recently executed process is appended at the end of ready_queue

                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                if ready_queue[0][2] > time_quantum:

                    #If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch

                    start_time.append(s_time)
                    s_time = s_time + time_quantum
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_quantum
                    ready_queue.pop(0)
                elif ready_queue[0][2] <= time_quantum:

                    #If a process has a remaining burst time less than or equal to time slice, it will complete its execution

                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                if normal_queue[0][2] > time_quantum:

                    #If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch

                    start_time.append(s_time)
                    s_time = s_time + time_quantum
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_quantum
                elif normal_queue[0][2] <= time_quantum:

                    #If a process has a remaining burst time less than or equal to time slice, it will complete its execution

                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
        t_time = RoundRobin.calculateTurnaroundTime(self, process_data)
        w_time = RoundRobin.calculateWaitingTime(self, process_data)
        RoundRobin.printData(self, process_data, t_time, w_time, executed_process)
        RoundRobin.drawGanttChart(self, process_data, executed_process, start_time, exit_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]

            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_TAT = total_turnaround_time / len(process_data)

        return average_TAT

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]

            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_WT = total_waiting_time / len(process_data)

        return average_WT

    def printData(self, process_data, average_TAT, average_WT, executed_process):
        process_data.sort(key=lambda x: x[0])
        print()

        #Sort processes according to the Process ID

        print("+==========+==================+===============+=============+===================+=====================+")
        print("| Process  | Arrival Time(ms)| Burst Time(ms) | End Time(ms)|Turnaround Time(ms)| Waiting Time(ms)    |")
        print("+==========+==================+===============+=============+===================+=====================+")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                if(j!=2 and j!=3):
                  print(process_data[i][j], end="		 ")
            print()

        print(f'Average Turnaround Time: {average_TAT}')

        print(f'Average Waiting Time: {average_WT}')

        print(f'Sequence of Processes: {executed_process}')
        print("+------------------------------+------------------------------+------------------------------+")
        print("+------------------------------+------------------------------+------------------------------+")
        print()

# The following lines should be at the same indentation level as the class definition
if __name__ == "__main__":
    no_of_processes = int(input("Enter number of processes: "))
    print("+---------------+---------------+-----------------+")
    print("+---------------+---------------+-----------------+")
    rr = RoundRobin()
    rr.processData(no_of_processes)
