from collections import deque
import heapq

def bfs(graph, start_node, search_node=None):
    # graph: a dictionary representing the graph to be traversed.
    # start_node: a string representing the starting node of the traversal.
    # search_node: an optional string representing the node being searched for in the graph.
    # Note: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    #The output depends on whether the search_node is provided or not:
        #1. If search_node is provided, the function returns 1 if the node is found during the search and 0 otherwise.
        #2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.

    #Useful code snippets (not necessary but you can use if required)
    visited = {}
    path = []
    for key in graph.keys():
        visited[key] = 'not_visited'
    
    queue = deque()
    visited[start_node] = 'visited'
    queue.append(start_node)
    while(queue or graph[start_node]):
        for neighbour in sorted(graph[start_node]):
            if visited[neighbour] == 'not_visited':
                queue.append(neighbour)
                visited[neighbour] = 'visited'
            if search_node and neighbour == search_node:
                return 1
        if queue:
            start_node = queue[0]
            path.append(queue.popleft())
        else:
            break
        
    if search_node is not None:
        return 0  # search node not found

    return path  # search node not provided, return entire path [list of nconst values of nodes visited]



def dfs(graph, start_node, visited=None, path=None, search_node=None):
    # graph: a dictionary representing the graph
    # start_node: the starting node for the search
    # visited: a set of visited nodes (optional, default is None)
    # path: a list of nodes in the current path (optional, default is None)
    # search_node: the node to search for (optional, default is None)
    # Note: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    # The function returns:
        # 1. If search_node is provided, the function returns 1 if the node is found and 0 if it is not found.
        # 2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.
    
        

    stack = [start_node]
    path = []
    visited = {}
    for key in graph.keys():
        visited[key] = 'not_visited'
    #visited[start_node] = 'visited'
        
    while stack:
        node = stack.pop()
        if(search_node and search_node == node):
            return 1
        if visited[node] == 'not_visited':
            path.append(node)
            visited[node] = 'visited'
            for neighbor in sorted(graph[node], reverse=True):
                if visited[neighbor] == 'not_visited':
                    stack.append(neighbor)
                    
    if search_node:
        return 0
                    
    return path


def dijkstra(graph, start_node, end_node):
    distances = {}
    for node in graph:
        distances[node] = float('inf')
    distances[start_node] = 0
    
    heap = [(0, start_node)]
    node_history = {node: None for node in graph}
    
    visited = set()
    
    hop_count = {node: 0 for node in graph}
    hop_count[start_node] = 0
    
    while heap:
        distance, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        
        visited.add(current_node)
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = node_history[current_node]
            path.reverse()
            return [path, distances[end_node], hop_count[end_node]]
        
        for neighbor, weight in graph[current_node].items():
            tentative_distance = distance + weight
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                node_history[neighbor] = current_node
                heapq.heappush(heap, (tentative_distance, neighbor))
                hop_count[neighbor] = hop_count[current_node] + 1
    return 0


def reverse_graph(graph):
    reversed_graph = {node: {} for node in graph}

    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor][node] = graph[node][neighbor]

    return reversed_graph



def kosaraju(graph):
    # graph: a dictionary representing the graph where the keys are the nodes and the values
            # are dictionaries representing the edges and their weights.
    #Note: Here you need to call dfs function multiple times so you can Implement seperate
         # kosaraju_dfs function if required.

    #The output:
        #list of strongly connected components in the graph,
          #where each component is a list of nodes. each component:[nconst2, nconst3, nconst8,...] -> list of nconst id's.
    stack = []
    visited = set()
    components = []
    reversed_graph = {}

    # First DFS to fill the stack with nodes ordered by finish time
    def first_dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                first_dfs(neighbor)
        stack.append(node)

    # Second DFS to get strongly connected components
    def second_dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph.get(node, {}):
            if neighbor not in visited:
                second_dfs(neighbor, component)

    # Run DFS on all nodes in the reverse order of finish time
    for node in sorted(graph.keys(), reverse=True):
        if node not in visited:
            first_dfs(node)

    # Run DFS on nodes in the order given by the stack
    visited.clear()
    reversed_graph = reverse_graph(graph)
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            second_dfs(node, component)
            components.append(component)

    return components

