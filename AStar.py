import heapq
import random


class AStar:
    def __init__(self):
        self.mandatory_positions = ['StandInit', 'Sit', 'SitRelax', 'Stand', 'StandZero', 'Crouch']
        self.intermediate_positions = [
            'ArmsOpening', 'DiagonalLeft', 'DiagonalRight', 'DoubleMovement', 'MoveBackward', 'MoveForward',
            'RightArm', 'RotationFootLLeg', 'RotationFootRLeg', 'RotationHandgunObject', 'UnionArms'
        ]

        self.estimated_costs = {}

        for pos in self.intermediate_positions + self.mandatory_positions:
            for tar in self.intermediate_positions + self.mandatory_positions:
                if pos not in self.estimated_costs.keys():
                    self.estimated_costs[pos] = {}
                if pos == tar:
                    self.estimated_costs[pos][tar] = float('inf')
                else:
                    self.estimated_costs[pos][tar] = random.random()

    def __call__(self, start, goal):
        # Initialize the open and closed sets
        open_set = []
        heapq.heappush(open_set, (0, start))  # 0 stands for the f_score
        came_from = {}  # For path reconstruction

        # Costs from start to a specific node
        g_score = {position: float('inf') for position in self.intermediate_positions + self.mandatory_positions}
        # initial values set to infinite except the start node
        g_score[start] = 0

        # Estimated total cost from start to goal through a node, g_score + heuristic
        f_score = {position: float('inf') for position in self.intermediate_positions + self.mandatory_positions}
        # initial values set to infinite except the start node
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            # Get the position in open set with the lowest F score
            current = heapq.heappop(open_set)[1]

            # Check the finish point
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.intermediate_positions:
                # Tentative G Score for the neighbor
                tentative_g_score = g_score[current] + self.heuristic(current, neighbor)

                # If tentative G Score is better than the recorded one
                if tentative_g_score < g_score[neighbor]:
                    # Record the best path
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [start, self.intermediate_positions[random.randint(0, len(self.intermediate_positions) - 1)]]

    @staticmethod
    def reconstruct_path(came_from, current):
        # Reconstruct the path
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    # Heuristic Function, the cost from position to the goal
    def heuristic(self, position, goal):
        # Example: return the estimated 'cost' or 'difficulty' of moving from 'position' to 'goal'
        # Hypothetical cost estimates between positions
        return self.estimated_costs[position][goal]
