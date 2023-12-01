import sys

import motion

import almath

import math

import time

from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints

    pNames = "Body"

    pStiffnessLists = 1.0

    pTimeLists = 1.0

    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def perform_rotation_foot_RLeg(robotIP, port):
    # Init proxies.

    try:

        motionProxy = ALProxy("ALMotion", robotIP, port)

    except Exception, e:

        print "Could not create proxy to ALMotion"

        print "Error was: ", e

    try:

        postureProxy = ALProxy("ALRobotPosture", robotIP, port)

    except Exception, e:

        print "Could not create proxy to ALRobotPosture"

        print "Error was: ", e

    # Set NAO in Stiffness On

    StiffnessOn(motionProxy)

    # Send NAO to Pose Init

    postureProxy.goToPosture("StandInit", 0.3)

    motionProxy.wbEnable(True)

    # Legs/Feet Configuration

    stateName = "Plane"

    supportLeg = "RLeg"

    motionProxy.wbFootState(stateName, supportLeg)

    stateName = "Fixed"

    supportLeg = "LLeg"

    motionProxy.wbFootState(stateName, supportLeg)

    # Cartesian foot trajectory

    # Warning: Needs a PoseInit before executing

    space = motion.FRAME_ROBOT

    axisMask = 63  # control all the effector's axes

    isAbsolute = False

    # Lower the Torso and move to the side

    effector = "Torso"

    path = [0.0, 0.00, 0.00, 0.0, 0.0, 0.05]

    timeList = 3.0  # seconds

    motionProxy.positionInterpolation(effector, space, path,

                                      axisMask, timeList, isAbsolute)

    time.sleep(3)  # wait a few seconds

    # Back to the inizial position

    postureProxy.goToPosture("StandInit", 0.25)

    motionProxy.wbEnable(False)

def main(robotIP,port):
    perform_rotation_foot_RLeg()


