class Robot:
    '''
    Instantiate a class to communicate with a web server designed to control Spot
    
    :param server_ip: The ip address of the web server
    :param: program_name the name of the program
    
    :type server_ip: str
    :type program_name: str
    '''
    def __init__(self, server_ip, program_name=''):
        self.server_ip = "http://" + server_ip + ":8000"
        self.program_name = program_name
        self.commands = []
        self.is_adding_commands = False

    def send_commands(self):
        import requests, json
        self.is_adding_commands = False
        try:
            response = requests.post(self.server_ip + "/program", data=json.dumps({'name': self.program_name, 'commands': self.commands}))
            is_valid = response.json()['valid']
            return is_valid
        except Exception as e:
            print(e)
        
    '''
    Sends a command to the server containing the command information using a post request
    '''
    def _add_command(self, command_info):
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
        self._add_command(command_info)
    
    '''
    Tells Spot to sit
    '''
    def sit(self):
        command_info = {
            'Command': 'sit'
        }
        self._add_command(command_info)
    
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
        pitch = float(pitch)
        yaw = float(yaw)
        roll = float(roll)
        command_info = {
            'Command': 'rotate',
            'Args': {
                'pitch': pitch,
                'yaw': yaw,
                'roll': roll
            }
        }
        self._add_command(command_info)
    
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
        x = float(x)
        y = float(y)
        z = float(z)
        command_info = {
            'Command': 'move',
            'Args': {
                'x': x,
                'y': y,
                'z': z
            }
        }
        self._add_command(command_info)

    '''
    Tells spot to wait for a specified amount of time

    :param time: the desired time to wait in seconds

    :type time: float
    '''
    def wait(self, time):
        time = float(time)
        command_info = {
            'Command': 'wait',
            'Args': {
                'time': time
            }
        }
        self._add_command(command_info)
        
    def send_file(self, path, type="file", main_filename="main.py"):
        import os, requests
        files = {}
        data = {
            "main": main_filename
        }
        assert main_filename.endswith(".py"), "Wrong filetype for main_filename! (needs .py)"
        if type == "file":
            assert path.endswith(".py"), "Wrong Filetype! (needs .py)"
            assert os.path.exists(path), "File does not exist!"
            files = {'file': open(path, 'rb')}
            data={'folder': False}
        elif type == "folder":
            assert os.path.exists(path), "Directory does not exist!"
            for file in os.listdir(path):
                files[file] = open(path + "\\" + file, 'rb')
        
        response = requests.post(self.server_ip + "/file", files=files, data=data)
        is_valid = response.json()['valid']
        return is_valid
