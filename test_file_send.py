from cc_spot_python import Robot
import time

robot = Robot('192.168.86.32', 'test')
path = 'C:\\Users\\willf\\OneDrive\\Documents\\GitHub\\python-spot-control\\tests'
robot.send_file(path, type="folder", main_filename="test.py")
