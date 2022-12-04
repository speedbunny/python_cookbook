class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

def shortest_path(source, target):
    """
    Returns the shortest list of (id1, id2) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """
    if source == target:
       raise Exception("Source is Target")
    frontier = QueueFrontier()
    # Start with a frontier that contains the initial state.
    start = Node(source, None, None)
    frontier.add(start)
    explored = ([])
    path = []
    while not frontier.empty():  # Repeat
        node = frontier.remove() # Remove node from frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action) 
                # Check if new nodes in frontier contain goal
                if child.state == target:
                    while child.parent is not None:
                        path.append((child.action, child.state))
                        child = child.parent
                    path.reverse()
                    #If node contains goal state, return the solution.
                    return path
                else:
                    #Expand node, add resulting nodes to the frontier.
                    frontier.add(child)
        # Add node to explored set
        explored.append(node.state)
        # If the frontier is empty, then no solution.
    return None
