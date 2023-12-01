from naoqi import ALProxy
from AStar import AStar
from RobotPositions import *
import time


MANDATORY_POSITIONS = ['StandInit', 'SitRelax', 'Sit', 'Stand', 'StandZero', 'Crouch']

# position base, with action and cost
intermediate_positions = {
    'StandInit': {'action': stand_init, 'cost': 0},
    'Sit': {'action': sit, 'cost': 9},
    'SitRelax': {'action': sit_relax, 'cost': 5},
    'Stand': {'action': stand, 'cost': 2},
    'StandZero': {'action': stand_zero, 'cost': 7},
    'Crouch': {'action': crouch, 'cost': 0},
    'ArmsOpening': {'action': arms_opening, 'cost': 5},
    'DiagonalLeft': {'action': diagonal_left, 'cost': 4},
    'DiagonalRight': {'action': diagonal_right, 'cost': 9},
    'DoubleMovement': {'action': double_movement, 'cost': 12},
    'MoveBackward': {'action': move_backward, 'cost': 18},
    'MoveForward': {'action': move_forward, 'cost': 3},
    'RightArm': {'action': right_arm, 'cost': 15},
    'RotationFootLLeg': {'action': rotation_foot_l_leg, 'cost': 11},
    'RotationFootRLeg': {'action': rotation_foot_r_leg, 'cost': 7},
    'RotationHandgunObject': {'action': rotation_handgun_object, 'cost': 14},
    'UnionArms': {'action': union_arms, 'cost': 16}
}


def main(motion_proxy, posture_proxy, tts_proxy):
    # Wake up NAO
    motion_proxy.wakeUp()
    path = calculate_path()
    perform_dance(path, motion_proxy, posture_proxy, tts_proxy)
    # NAO rest
    motion_proxy.rest()


def calculate_path():
    print "Start Calculating"
    path = []
    a_star = AStar()
    for idx in range(len(MANDATORY_POSITIONS) - 1):
        path.extend(a_star(MANDATORY_POSITIONS[idx], MANDATORY_POSITIONS[idx + 1]))
    if path[-1] != MANDATORY_POSITIONS[-1]:
        path.append(MANDATORY_POSITIONS[-1])
    return path


# function to perform the dance
def perform_dance(path, motion_proxy, posture_proxy, tts_proxy):
    motion_proxy.setStiffnesses("Body", 1.0)
    motion_proxy.post.angleInterpolation(["HeadPitch", "HeadYaw"], [[0.5, -0.5], [0.5, -0.5]], [1, 2], False)
    motion_proxy.waitUntilMoveIsFinished()
    start_time = time.time()
    print "Start performing"
    print "Path found:", " -> ".join(path)
    for position in path:
        if position in intermediate_positions:
            intermediate_positions[position]['action'](motion_proxy, posture_proxy, tts_proxy)
            # action(nao_ip, nao_port)  # Execute the position's action
    end_time = time.time() - start_time
    print "end performing: " + str(end_time) + "s"


if __name__ == "__main__":
    # IP and Port of NAO
    nao_ip = "houtongdemacbook-pro.local."
    nao_port = 9559

    # Connect to the motion and posture proxy
    motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
    postureProxy = ALProxy("ALRobotPosture", nao_ip, nao_port)
    ttsProxy = ALProxy("ALTextToSpeech", nao_ip, nao_port)

    main(motionProxy, postureProxy, ttsProxy)
