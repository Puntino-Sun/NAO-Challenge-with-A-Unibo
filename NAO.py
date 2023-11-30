from naoqi import ALProxy
import time
import sys
import motion
import almath
import networkx
import heapq
from search_algorithm import A_star
from arms_opening import perform_arms_opening
from Diagonal_left import perform_Diagonal_left
from Diagonal_right import perform_Diagonal_right
from double_movement import perform_double_movement
from move_backward import perform_move_backward
from move_forward import perform_move_forward
from right_arm import perform_right_arm
from Rotation_foot_LLeg import perform_rotation_foot_LLeg
from Rotation_foot_RLeg import perform_rotation_foot_RLeg
from rotation_handgun_object import perform_rotation_handgun_object
from union_arms import perform_union_arms

# IP and Port of NAO
nao_ip = "127.0.0.1"
nao_port = int(input("Please input the port:"))
# Connect to the motion and posture proxy
motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
posture_proxy = ALProxy("ALRobotPosture", nao_ip, nao_port)

# position base, with action and cost
intermediate_positions = {
        'arms_opening': {
            'action': perform_arms_opening(nao_ip,nao_port),
            'cost': 5
        },
        'Diagonal_left': {
            'action': perform_Diagonal_left(nao_ip,nao_port),
            'cost': 4
        },
        'Diagonal_right': {
            'action': perform_Diagonal_right(nao_ip,nao_port),
            'cost': 9
        },
        'double_movement': {
            'action': perform_double_movement(nao_ip,nao_port),
            'cost': 12
        },
        'move_backward': {
            'action': perform_move_backward(nao_ip,nao_port),
            'cost': 18
        },
        'move_forward': {
            'action': perform_move_forward(nao_ip,nao_port),
            'cost': 3
        },
        'right_arm': {
            'action': perform_right_arm(nao_ip,nao_port),
            'cost': 15
        },
        'Rotation_foot_LLeg': {
            'action': perform_rotation_foot_LLeg(nao_ip,nao_port),
            'cost': 11
        },
        'Rotation_foot_Rleg': {
            'action': perform_rotation_foot_RLeg(nao_ip,nao_port),
            'cost': 7
        },
        'rotation_handgun_object': {
            'action': perform_rotation_handgun_object(nao_ip,nao_port),
            'cost': 14
        },
        'union_arms': {
            'action': perform_union_arms(nao_ip,nao_port),
            'cost': 16
        }
    }

# A* Algorithm
def A_star(start, goal, dance_positions, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))  # 0 stands for the f_score
    came_from = {}  # For path reconstruction

    # Costs from start to a specific node
    g_score = {position: float('inf') for position in dance_positions} # initial values set to infinite except the start node
    g_score[start] = 0

    # Estimated total cost from start to goal through a node, g_score + heuristic
    f_score = {position: float('inf') for position in dance_positions} # initial values set to infinite except the start node
    f_score[start] = heuristic(start, goal)

    while open_set:
        # Get the position in open set with the lowest F score
        current = heapq.heappop(open_set)[1]

        # Check the finish point
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in dance_positions[current]:
            # Tentative G Score for the neighbor
            tentative_g_score = g_score[current] + dance_positions[current][neighbor]

            # If tentative G Score is better than the recorded one
            if tentative_g_score < g_score[neighbor]:
                # Record the best path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Path not found

def reconstruct_path(came_from, current):
    # Reconstruct the path
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

# Heuristic Function, the cost from position to the goal
def heuristic(position, goal):
    # Hypothetical cost estimates between positions, self defined
    estimated_costs = {
        'arms_opening': {'Diagonal_left': 5, 'Diagonal_right': 5, 'double_movement': 7},
        'Diagonal_left': {'arms_opening': 5, 'move_backward': 3, 'move_forward': 4},
        'Diagonal_right': {'arms_opening': 5, 'move_backward': 4, 'move_forward': 3},
        'double_movement': {'arms_opening': 7, 'right_arm': 6},
        'move_backward': {'arms_opening': 6, 'rotation_handgun_object': 8, 'Rotation_foot_LLeg': 3},
        'move_forward': {'Rotation_foot_RLeg': 2, 'right_arm': 3},
        'right_arm': {'double_movement': 9, 'move_backward': 5, 'Diagonal_right': 4},
        'Rotation_foot_LLeg': {'Rotation_foot_RLeg': 1, 'arms_opening': 3},
        'Rotation_foot_RLeg': {'Rotation_foot_LLeg': 1, 'Diagonal_right': 3, 'rotation_handgun_object': 4},
        'rotation_handgun_object': {'move_forward': 5, 'union_arms': 8},
        'union_arms': {'right_arm': 8, 'move_backward': 4, 'rotation_handgun_object': 3}

    }

    return estimated_costs.get(position, {}).get(goal, 10)
    pass

# function to perform the dance
def perform_dance(start_position, end_position):
    motion_proxy.setStiffnesses("Body", 1.0)
    motion_proxy.post.angleInterpolation(["HeadPitch", "HeadYaw"], [[0.5, -0.5], [0.5, -0.5]], [1, 2], False)
    motion_proxy.waitUntilMoveIsFinished()

    path = A_star(start_position, end_position, intermediate_positions, heuristic)

    if path:
        print("Path found:", " -> ".join(path))
        for position in path:
            if position in intermediate_positions:
                action = intermediate_positions[position]['action']
                action(nao_ip, nao_port)  # Execute the position's action
    else:
        print("No path found from {} to {}".format(start_position, end_position))





# Main
if __name__ == "__main__":
    # Wake up NAO
    motion_proxy.wakeUp()

    perform_dance('arms_opening','move_forward')

    # NAO rest
    motion_proxy.rest()

