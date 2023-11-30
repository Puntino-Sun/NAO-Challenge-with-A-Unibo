import heapq
# A* Algorithm Implementation
def A_star(start, goal, dance_positions, heuristic):
    # Initialize the open and closed sets
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}  # For path reconstruction

    # Costs from start to a node
    g_score = {position: float('inf') for position in dance_positions}
    g_score[start] = 0

    # Estimated total cost from start to goal through a node
    f_score = {position: float('inf') for position in dance_positions}
    f_score[start] = heuristic(start, goal)

    while open_set:
        # Get the position in open set with the lowest F score
        current = heapq.heappop(open_set)[1]

        # Check if the goal is reached
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in dance_positions[current]:
            # Tentative G Score for the neighbor
            tentative_g_score = g_score[current] + dance_positions[current][neighbor]

            # If tentative G Score is better than the recorded one
            if tentative_g_score < g_score[neighbor]:
                # This path is the best so far, record it
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Path not found

def reconstruct_path(came_from, current):
    # Reconstruct the path found
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

# Heuristic Function
def heuristic(position, goal):
    # Example: return the estimated 'cost' or 'difficulty' of moving from 'position' to 'goal'
    # Hypothetical cost estimates between positions
    estimated_costs = {
        'arms_opening': {'diagonal_left': 5, 'diagonal_right': 5, 'double_movement': 7},
        'diagonal_left': {'arms_opening': 5, 'move_backward': 3, 'move_forward': 4},
        'diagonal_right': {'arms_opening': 5, 'move_backward': 4, 'move_forward': 3},
        'double_movement': {'arms_opening': 7, 'right_arm': 6},
        # ... (add estimates for other positions)
    }

    return estimated_costs.get(position, {}).get(goal, 10)
    pass