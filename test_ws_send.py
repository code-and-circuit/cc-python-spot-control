from cc_spot import Robot
import math
import time

robot = Robot()

robot.connect('Will')
robot.stand()
robot.keep_alive_until_done()
