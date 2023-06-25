from cc_spot import Robot
import time

robot = Robot()
robot.start_program('Will')
robot.sit()
robot.wait(1)
robot.stand()
robot.wait(1)
robot.walk(-1, 0, 0)
robot.send_program()
