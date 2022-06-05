def solution(entrances, exits, path):
    # Your code here
    n = len(path) + 2
    src = n - 2
    dst = n - 1
    capacity = list()
    used = list()
    
    # init capacity and used
    for _ in range(n):
        capacity.append([0 for _ in range(n)])
        used.append([0 for _ in range(n)])

    for i in range(len(path)):
        for j in range(len(path)):
            capacity[i][j] = path[i][j]
    for pos in entrances:
        capacity[src][pos] = 'inf'
    for pos in exits:
        capacity[pos][dst] = 'inf'

    def find_a_flow():
        flow = [src]
        visited = [False for _ in range(n)]
        visited[src] = True

        def dfs(bottle_neck):
            last_stop = flow[-1]

            for i in range(n):
                if i == dst and capacity[last_stop][i] == 'inf':
                    return bottle_neck
                
                if not visited[i]:
                    choose_i = False
                    if capacity[last_stop][i] == 'inf':
                        choose_i = True
                    else:
                        max_flow_for_this_pipe = capacity[last_stop][i] - used[last_stop][i]
                        choose_i = max_flow_for_this_pipe > 0
                        # print(choose_i, max_flow_for_this_pipe)
                    if choose_i:
                        flow.append(i)
                        visited[i] = True
                        old_bottle_neck = bottle_neck
                        if capacity[last_stop][i] == 'inf':
                            pass
                        elif bottle_neck == 'inf':
                            bottle_neck = max_flow_for_this_pipe
                        else:
                            bottle_neck = min(max_flow_for_this_pipe, bottle_neck)

                        res = dfs(bottle_neck)
                        if res:
                            return res
                        else:
                            bottle_neck = old_bottle_neck
                            visited[i] = False
                            flow.pop()
                            continue

        res = dfs('inf')
        # print(res, flow)
        if res:
            for i in range(1, len(flow) - 1):
                used[flow[i]][flow[i + 1]] += res
                used[flow[i + 1]][flow[i]] -= res
            return res
        else:
            return 0
        


    max_flow = 0
    while True:
        new_flow = find_a_flow()
        if new_flow == 0:
            return max_flow
        else:
            max_flow += new_flow
    


print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))
