class RoundRobin:

    def processData(self, no_of_processes):
        process_data = []

        for i in range(no_of_processes):
            temporary = []
            process_id = i + 1
            arrival_time = int(input(f" P[{process_id}] Arrival Time: "))
            burst_time = int(input(f" P[{process_id}] Burst Time: "))
            print("==========================================================================")
            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])  # '0' is the state of the process
            process_data.append(temporary)

        time_quantum = int(input("Enter Time Quantum: "))
        self.schedulingProcess(process_data, time_quantum)

    def drawGanttChart(self, executed_process, start_time, exit_time):
        print("\n=================== GANTT CHART (Round Robin) =======================")
        for pid in executed_process:
            print(f"| P{pid} ", end="")
        print("|")

        for time in start_time:
            print(f"{time:>3}", end=" ")
        print(f"{exit_time[-1]:>3}")  # Print the end time of the last process

    def schedulingProcess(self, process_data, time_quantum):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])  # Sort by Arrival Time

        while True:
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    ready_queue.append(process_data[i])
                    process_data[i][3] = 1  # Mark as considered

            if not ready_queue:
                waiting_processes = [p[1] for p in process_data if p[3] == 0]
                if waiting_processes:
                    s_time = min(waiting_processes)
                    continue
                else:
                    break  # All processes have been executed

            current_process = ready_queue.pop(0)
            start_time.append(s_time)

            if current_process[2] > time_quantum:
                s_time += time_quantum
                current_process[2] -= time_quantum
                executed_process.append(current_process[0])
                exit_time.append(s_time)
                ready_queue.append(current_process)  # Re-add to the queue
            else:
                s_time += current_process[2]
                executed_process.append(current_process[0])
                exit_time.append(s_time)
                current_process[2] = 0  # Complete the execution
                current_process[3] = 2  # Mark as completed
                current_process.append(s_time)  # Add completion time

        t_time = self.calculateTurnaroundTime(process_data)
        w_time = self.calculateWaitingTime(process_data)
        self.printData(process_data, t_time, w_time, executed_process)
        self.drawGanttChart(executed_process, start_time, exit_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]  # End Time - Arrival Time
            total_turnaround_time += turnaround_time
            process_data[i].append(turnaround_time)
        average_TAT = total_turnaround_time / len(process_data)
        return average_TAT

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]  # Turnaround Time - Burst Time
            total_waiting_time += waiting_time
            process_data[i].append(waiting_time)
        average_WT = total_waiting_time / len(process_data)
        return average_WT

    def printData(self, process_data, average_TAT, average_WT, executed_process):
        process_data.sort(key=lambda x: x[0])  # Sort processes according to the Process ID

        print("\n======================== ROUND ROBIN SCHEDULING =========================\n")
        print("+------------+------------------+----------------+---------------+---------------------+-------------------+")
        print("| Process    | Arrival Time(ms) | Burst Time(ms) | End Time(ms) | Turnaround Time(ms) | Waiting Time(ms)   |")
        print("+------------+------------------+----------------+---------------+---------------------+-------------------+")


        for data in process_data:
            end_time = data[5] if len(data) > 5 else 0
            turnaround_time = data[6] if len(data) > 6 else 0
            waiting_time = data[7] if len(data) > 7 else 0

            print(f"|    P{data[0]:<6} | {data[1]:<16} | {data[2]:<14} | {end_time:<13} | {turnaround_time:<19} | {waiting_time:<17} |")
            print("+------------+------------------+----------------+---------------+---------------------+-------------------+")

            
        print(f'\nAverage Turnaround Time: {average_TAT:.2f}')
        print(f'Average Waiting Time: {average_WT:.2f}')
        print(f'Sequence of Processes: {executed_process}')
        print("==========================================================================")


if __name__ == "__main__":
    no_of_processes = int(input("Enter number of processes: "))
    rr = RoundRobin()
    rr.processData(no_of_processes)
