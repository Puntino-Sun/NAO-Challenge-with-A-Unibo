import sys

import motion

import almath

import math

import time

from naoqi import ALProxy

def perform_Diagonal_right(robotIP, port):
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
    ttsProxy.say("Diagonal right")
    time.sleep(1)

    # Set NAO in Stiffness On

    #    StiffnessOn(motionProxy)

    distance_x_m = 0.03
    distance_y_m = -0.012
    theta_deg = 0.0
    # The command position estimation will be set to the sensor position when the robot starts moving, so we use sensors first and commands later.
    initPosition = almath.Pose2D(motionProxy.getRobotPosition(True))
    targetDistance = almath.Pose2D(distance_x_m, distance_y_m, theta_deg * almath.PI / 180)
    expectedEndPosition = initPosition * targetDistance
    enableArms = 0
    motionProxy.setMoveArmsEnabled(enableArms, enableArms)
    motionProxy.moveTo(distance_x_m, distance_y_m, theta_deg)

def main(robotIP,port):
    perform_Diagonal_right()