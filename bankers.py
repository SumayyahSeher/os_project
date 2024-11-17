def get_input():
    proc= int(input("Enter number of processes: "))
    res= int(input("Enter number of resources: "))

    allocation= []

    print("Enter allocations for each process -Allocation Matrix: ")

    for i in range(proc):
        allocated= input(f"P [{i}]: ")
        allocated_list=[int(ele) for ele in allocated.split()]
        allocation.append(allocated_list)


    max=[]

    print("Enter maximum requests for each process -Max Matrix: ")

    for i in range(proc):
        max_req= input(f"P [{i}]: ")
        max_req_list=[int(ele) for ele in max_req.split()]
        max.append(max_req_list)

    available_res= input("Enter available matrix: ")
    available= [int(ele) for ele in available_res.split()]

    return proc,res,allocation,max,available


def calculate_need(proc, res, allocation, max):
    need=[]
    for i in range (proc):
        resource=[]
        for j in range(res):
            resource.append(0)
        need.append(resource)

    for i in range (proc):
        for j in range(res):    
            need[i][j]= max[i][j]-allocation[i][j]

    return need


def safe_check(proc, res, allocation, need, available):
    work=available[:]
    finish = [False] * proc
    safe_sequence = []

    
    while len(safe_sequence)<proc:
        found=False
        for i in range(proc):
            if finish[i]==False:
                can_allocate=True
                for j in range(res):
                    if need[i][j] > work[j]:
                        can_allocate=False
                        break

                if can_allocate:
                    safe_sequence.append(i)
                    finish[i] = True
                    found = True
                    for k in range(res):
                        work[k] += allocation[i][k]

        if (found == False):
            print("System is not in safe state")
            return False    

    print("System is in safe state.",
           "\nSafe sequence is: ", end = " ")
    print(safe_sequence) 
 
    return True


def request_resources(process_num, request, proc, res, allocation, need, available):


    can_grant=True
    for j in range(res):
        if request[j]>need[process_num][j] or request[j]>available[j]:
            can_grant= False
            break

    if can_grant:
        for j in range(res):
            available[j] -= request[j]
            allocation[process_num][j] += request[j]
            need[process_num][j] -= request[j]

        is_safe= safe_check(proc, res, allocation, need, available)

        if is_safe==False:
            for j in range(res):
                available[j] += request[j]
                allocation[process_num][j] -= request[j]
                need[process_num][j] += request[j]
            return False
        
        return True
    
    return False

def print_matrix(proc, res,  allocation, max_matrix, available, need):

    headers = ["Process", "Allocation", "Max", "Need", "Available"]

    process_width= len(headers[0]) #width of column header
    resource_width= max(10, 2 * res - 1) # dynamic calculation of colum widths based on number of resources

    row_format = (
        f"| {{:<{process_width}}} | {{:<{resource_width}}} | {{:<{resource_width}}} | {{:<{resource_width}}} | {{:<{resource_width}}} |"
    )

    border= ("+="+ "="*process_width+ "=+="+ "="*resource_width+ "=+="+ "="*resource_width+ "=+="+ "="*resource_width+ "=+="+ "="*resource_width+ "=+")

    print(border)
    print(row_format.format(*headers))
    print(border)

    for i in range(proc):
        print(row_format.format(
            f"P[{i}]",
            ' '.join(map(str, allocation[i])),
            ' '.join(map(str, max_matrix[i])),
            ' '.join(map(str, need[i])),
            ' '.join(map(str, available)) if i == 0 else ""
        ))

    print(border)


def banker_main():
    proc, res, allocation, max, available =get_input()

    need= calculate_need(proc, res, allocation, max)

    print_matrix(proc, res,  allocation, max, available, need)

    safe=safe_check(proc, res, allocation, need, available)

    if safe:

        while True:
            choice = input("Do you want to make a resource request? (yes/no): ").strip().lower()
            if choice != 'yes':
                break
            
            process_num = int(input("Enter process number: "))

            req_input= input("Enter available matrix: ")
            request= [int(ele) for ele in req_input.split()]

            if request_resources(process_num, request, proc, res, allocation, need, available):
                print("Request granted.")
                print("Here are the update matrices")
                print_matrix(proc, res,  allocation, max, available, need)

            else:
                print("Request cannot be granted. Causes unsafe state.")

