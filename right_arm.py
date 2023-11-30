import sys

import motion

import almath

import time

from naoqi import ALProxy

def perform_right_arm(robotIP, port):
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

    try:
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ", e

    # Set NAO in Stiffness On

    #    StiffnessOn(motionProxy)

    # NAO:
    ttsProxy.say(
        "right arm")
    time.sleep(1)

    #    # Go to the Initial Position
    #    postureProxy.post.goToPosture("StandInit", 0.8)
    ##    RHand = 0.10
    #    motionProxy.post.angleInterpolation("RHand", 0.10, 0.1, True)
    #    time.sleep(3)
    # Moving

    ########## Start position ###########

    RShoulderPitch = 78.0

    RShoulderRoll = -16.6

    RElbowYaw = 68.3

    RElbowRoll = 49.2

    RWristYaw = 4.3

    RHand = 0.10

    LShoulderPitch = 78.0

    LShoulderRoll = 16.6

    LElbowYaw = -68.3

    LElbowRoll = -49.2

    LWristYaw = 4.3

    LHand = 0.0

    names = "LArm"

    angleLists = [LShoulderPitch * almath.TO_RAD, LShoulderRoll * almath.TO_RAD, LElbowYaw * almath.TO_RAD,

                  LElbowRoll * almath.TO_RAD, LWristYaw * almath.TO_RAD, LHand]

    timeLists = 2

    motionProxy.post.angleInterpolation(names, angleLists, timeLists, True)

    names = "RArm"

    angleLists = [RShoulderPitch * almath.TO_RAD, RShoulderRoll * almath.TO_RAD, RElbowYaw * almath.TO_RAD,

                  RElbowRoll * almath.TO_RAD, RWristYaw * almath.TO_RAD, RHand]

    timeLists = 2

    motionProxy.angleInterpolation(names, angleLists, timeLists, True)

    # Not waiting because movement is fluid and without pause

    ########## Movement arms ###########

    # Open/extend RArm

    RShoulderPitch = -75.7

    RShoulderRoll = -79.8

    RElbowYaw = -57.6

    RElbowRoll = 2.2

    RWristYaw = 87.0

    RHand = 0.35

    names = "RArm"

    angleLists = [RShoulderPitch * almath.TO_RAD, RShoulderRoll * almath.TO_RAD, RElbowYaw * almath.TO_RAD,

                  RElbowRoll * almath.TO_RAD, RWristYaw * almath.TO_RAD, RHand * almath.TO_RAD]

    motionProxy.setAngles(names, angleLists, 0.1)

    time.sleep(2)

    # Raise RArm sideways

    RShoulderPitch = -79.8

    RShoulderRoll = -26.2

    RElbowYaw = -57.6

    RElbowRoll = 2.2

    RWristYaw = 87.0

    RHand = 0.35

    names = "RArm"

    angleLists = [RShoulderPitch * almath.TO_RAD, RShoulderRoll * almath.TO_RAD, RElbowYaw * almath.TO_RAD,

                  RElbowRoll * almath.TO_RAD, RWristYaw * almath.TO_RAD, RHand * almath.TO_RAD]

    motionProxy.setAngles(names, angleLists, 0.15)

    time.sleep(1)

    # Align RShoulder and move forward RArm

    RShoulderPitch = 11.0

    RShoulderRoll = 5.4

    RElbowYaw = 68.3

    RElbowRoll = 2.2

    RWristYaw = 88.5

    RHand = 0.35

    names = "RArm"

    angleLists = [RShoulderPitch * almath.TO_RAD, RShoulderRoll * almath.TO_RAD, RElbowYaw * almath.TO_RAD,

                  RElbowRoll * almath.TO_RAD, RWristYaw * almath.TO_RAD, RHand * almath.TO_RAD]

    timeLists = 4

    motionProxy.angleInterpolation(names, angleLists, timeLists, True)

def main(robotIP,port):
    perform_right_arm()


#    # Go to the Initial Position
#    postureProxy.goToPosture("StandInit", 0.8)


