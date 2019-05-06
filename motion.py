### Motion planning on a rectangular grid

from random import random
from random import seed
from Queue import PriorityQueue
from copy import deepcopy


class State(object):
    
    def __init__(self, start_position, goal_position, start_grid):
        self.position = start_position
        self.goal = goal_position
        self.grid = start_grid
        self.total_moves = 0
        self.moves_list = [(start_position)]
        
    #--- Fill in the rest of the class...
    def manhattan_distance(self):
        return self.goal[0] - self.position[0] + self.goal[1] - self.position[1]

def create_grid():
    
    """Create and return a randomized grid
    
        0's in the grid indcate free squares
        1's indicate obstacles
        
        DON'T MODIFY THIS ROUTINE.
    """
    
    # Start with a num_rows by num_cols grid of all zeros
    grid = [[0 for c in range(num_cols)] for r in range(num_rows)]
    
    # Put ones around the boundary
    grid[0] = [1 for c in range(num_cols)]
    grid[num_rows - 1] = [1 for c in range(num_cols)]

    for r in range(num_rows):
        grid[r][0] = 1
        grid[r][num_cols - 1] = 1
            
    # Sprinkle in obstacles randomly
    for r in range(1, num_rows - 1):
        for c in range(2, num_cols - 2):
            if random() < obstacle_prob:
                grid[r][c] = 1;

    # Make sure the goal and start spaces are clear
    grid[1][1] = 0
    grid[num_rows - 2][num_cols - 2] = 0
            
    return grid
    

def print_grid(grid):
    
    """Print a grid, putting spaces in place of zeros for readability
    
       DON'T MODIFY THIS ROUTINE.
    """
    
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r][c] == 0:
                print ' ',  # Ending comma prevents automatic newline
            else:
                print grid[r][c],
        print ''
            
    print ''

    return 

def adjacent_to(maze_dim, i, j):
    
    """Return a list of possible next cells
    """
    neighbors = (
        (i - 1, j),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j))
    return [p for p in neighbors if 0 <= p[0] < maze_dim[0] and 0 <= p[1] < maze_dim[1]]
    
def manhattan_distance(position, goal):
    return goal[0] - position[0] + goal[1] - position[1]


def main():
    
    # Setup the randomized grid
    grid = create_grid()
    print_grid(grid)
    
    # Initialize the starting state and priority queue
    start_position = (1, 1)
    goal_position = (num_rows - 2, num_cols - 2)
    start_state = State(start_position, goal_position, grid)
    start_state.grid[1][1] = '*'
    priority = start_state.total_moves + start_state.manhattan_distance()
    
    queue = PriorityQueue()
    
    # Insert as a tuple
    # The queue orders elements by the first tuple value
    # A call to queue.get() returns the tuple with the minimum first value
    queue.put((priority, start_state))
    
    # Maybe you need a dictionary of previously visited positions?
    visited = {}
    best_path = {}
    
    #--- Fill in the rest of the search...
    maze_dims = (len(start_state.grid), len(start_state.grid[0]))
    
    while not queue.empty():
        curr_node = queue.get()
        
        if curr_node[1].position == goal_position:
            print curr_node[1].total_moves, len(curr_node[1].moves_list), curr_node[1].moves_list
            
            current = curr_node[1].position
            path = [current]
            while current != start_position:
                start_state.grid[1][1] = '*'
                curr_node[1].grid[current[0]][current[1]] = '*'
                current = visited[current]
                path.append(current)

            print_grid(curr_node[1].grid)
            
            return 
        for adj_cell in adjacent_to(maze_dims, curr_node[1].position[0], curr_node[1].position[1]):
            adj_cell_passable = curr_node[1].grid[adj_cell[0]][adj_cell[1]]
            if adj_cell not in visited and adj_cell_passable == 0:
                next_state = State(adj_cell, goal_position, curr_node[1].grid)
                next_state.total_moves = curr_node[1].total_moves + 1
                
                visited[adj_cell] = curr_node[1].position
                priority = next_state.total_moves + next_state.manhattan_distance()
                
                next_state.moves_list.append(adj_cell)
                queue.put((priority, next_state))
                
    print 'No possible solution to this maze!!!'

if __name__ == '__main__':
    
    seed(0)
    
    #--- Easy mode
    
    # Global variables --- saves us the trouble of continually passing them as
    # parameters to every routine
    num_rows = 8
    num_cols = 16
    obstacle_prob = .20
    
    for trial in range(5):
        print '\n\n-----Easy trial ' + str(trial + 1) + '-----'
        main()
        
    #--- Uncomment the following sets of trials when you're ready
        
    #--- Hard mode
    num_rows = 15
    num_cols = 30
    obstacle_prob = .30
    
    for trial in range(5):
        print '\n\n-----Harder trial ' + str(trial + 1) + '-----'
        main()
        
    #--- INSANE mode
    num_rows = 20
    num_cols = 60
    obstacle_prob = .35
    
    for trial in range(5):
        print '\n\n-----INSANE trial ' + str(trial + 1) + '-----'
        main()
