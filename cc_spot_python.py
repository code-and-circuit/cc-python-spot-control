import requests, json

class Robot:
    '''
    Instantiate a class to communicate with a web server designed to control Spot
    
    :param server_ip: The ip address of the web server
    :param: program_name the name of the program
    
    :type server_ip: str
    :type program_name: str
    '''
    def __init__(self, server_ip, program_name):
        self.server_ip = "http://" + server_ip + ":8000/program"
        self.program_name = program_name
        self.commands = []
        self.is_adding_commands = False

    def send_commands(self):
        self.is_adding_commands = False
        try:
            response = requests.post(self.server_ip, data=json.dumps({'name': self.program_name, 'commands': self.commands}))
            is_valid = response.json()['valid']
            return is_valid
        except Exception as e:
            print(e)
        
    '''
    Sends a command to the server containing the command information using a post request
    '''
    def add_command(self, command_info):
        if self.is_adding_commands:
            self.commands.append(command_info)

    '''
    Signifies the start of a command chunk and allows commands to be added
    '''
    def start_commands(self):
        self.is_adding_commands = True
        
    '''
    Tells Spot to stand
    '''
    def stand(self):
        command_info = {
            'Command': 'stand'
        }
        self.add_command(command_info)
    
    '''
    Tells Spot to sit
    '''
    def sit(self):
        command_info = {
            'Command': 'sit'
        }
        self.add_command(command_info)
    
    '''
    Tells spot to rotate in a specified direction
    
    :param pitch: the desired pitch of the robot in degrees
    :param yaw: the desired yaw of the robot in degrees
    :param roll: the desired roll of the robot in degrees
    
    :type pitch: float
    :type yaw: float
    :type roll: float
    '''
    def rotate(self, pitch, yaw, roll):
        command_info = {
            'Command': 'rotate',
            'Args': {
                'pitch': pitch,
                'yaw': yaw,
                'roll': roll
            }
        }
        self.send_command(command_info)
    
    '''
    Tells spot to walk in a specified direction. Distance = 1m
    
    :param x: the desired x component robot's walking velocity
    :param y: the desired y component robot's walking velocity
    :param z: the desired body turn of robot
    
    :type x: float
    :type y: float
    :type z: float
    '''
    def walk(self, x, y, z):
        command_info = {
            'Command': 'move',
            'Args': {
                'x': x,
                'y': y,
                'z': z
            }
        }
        self.add_command(command_info)

    '''
    Tells spot to wait for a specified amount of time

    :param time: the desired time to wait in seconds

    :type time: float
    '''
    def wait(self, time):
        command_info = {
            'Command': 'wait',
            'Args': {
                'time': time
            }
        }
        self.add_command(command_info)
    
