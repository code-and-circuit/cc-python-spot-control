# Code & Circuit's Spot Python Module
A Python library to interact with Code & Circuit's Spot Web Server to allow easy control of the robot to people of any skill level in python. Refer to the server's [readme](https://github.com/code-and-circuit/spot-web-server) for related information and concepts.

This library works by packaging commands into a program (consisting of a list of commands) that is sent to the web server to be managed and run there. In the future, commands may be sent directly without being packaged into a program.

# The Basics
Refer to the program-sending [test file](https://github.com/code-and-circuit/cc-python-spot-control/blob/main/test_command_send.py) and the file-sending [test file](https://github.com/code-and-circuit/cc-python-spot-control/blob/main/test_file_send.py) for examples of how to use the python module.

To create an interface between the program and the web server, create an instance of the Robot class. The constructor takes two parameters: 
1. ```server_ip``` - the ip address to send information to
2. ```program_name``` - a name to associate with the program being sent.

The code could look something like this:
```
robot = Robot('192.168.86.32', 'test')
```

## Creating a Program
As mentioned previously, commands are packaged into programs and cannot be sent directly to the server. To start adding commands to the program, call ```robot.start_commands()```. This allows all following commands to be packaged together. To end a program and send it to the server, call ```robot.send_commands()```.

Example:
```
robot = Robot('192.168.86.32', 'test')
robot.start_commands()
robot.stand()
robot.wait(1)
robot.sit()
robot.send_commands()
```

### Available Motor Controls
- ```stand``` tells Spot to stand
  - Args: none
- ```sit``` tells Spot to sit
  - Args: none
- ```rotate``` tells Spot to rotate his body at a specified angle
  - Args:
    - ```pitch``` the desired pitch, in degrees
    - ```yaw``` the desired yaw, in degrees
    - ```roll``` the desired roll, in degrees
  - Note: Spot has limits as to how far he can rotate in certain directions. Passing a number too large will result in it being clamped.
- ```walk``` tells Spot to walk in a specified direction
  - Args:
    - ```x``` the distance along the direction of Spot's length
    - ```y``` the distance along the direction of Spot's width
    - ```z``` the desired turn of Spot's body direction, in degrees
  - Note: The units for x and y distance are fairly arbitrary as Spot will not move at exact distances. Play around with the parameters to get a feel for how they work
- ```wait``` tells the program to wait a specified duration before executing the subsequent command
  - Args:
    - ```time``` the desired wait time, in seconds

Example code:
```
robot = Robot('192.168.86.32', 'testAll')
robot.start_commands()
robot.stand()
robot.wait(1)
robot.rotate(45, 45, 45)
robot.wait(1)
robot.rotate(0, 0, 0)
robot.wait(1)
robot.walk(1, 1, 1)
robot.wait(1)
robot.sit()
robot.send_commands()
```

### Sending Files
The module also allows for individual files or entire folders to be uploaded to the server and run. 

**IMPORTANT: This results in very unsafe code, make sure that whoever is sending the files is not doing anything malicious**

All files (or folders) uploaded must contain a function, ```main```, which acts as the entry point for the program. The ```main``` function is called in whichever file is specified as the "main file".

Services to control Spot can be imported using the following statement:
```
from SpotSite.background_process import bg_process
```

The ```bg_process``` object has many different services and useful information as attributes which can be found by looking at its [source code](https://github.com/code-and-circuit/spot-web-server/blob/main/WebPage/SpotSite/background_process.py), under the class ```Background_Process```.

There is one function to send a file or folder to the server: ```send_file```.

Args:
  - ```path``` the path to the file or folder
  - ```type``` the type of the data being sent, in the form of a string (either ```"file"``` or ```"folder"```
    - Defaults to: ```"file"```
  - ```main_filename``` the file containg the entry function for the program
    - Defaults to: ```"main.py"```

  



