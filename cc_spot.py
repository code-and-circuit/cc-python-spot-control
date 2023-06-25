import requests
import json
import websockets
from threading import Thread
from websockets.sync.client import connect
import asyncio
import time


class Robot:
    '''
    Instantiate a class to communicate with a web server designed to control Spot

    :param server_ip: The ip address of the web server
    :param: program_name the name of the program

    :type server_ip: str
    :type program_name: str
    '''

    def __init__(self, server_ip='192.168.4.55:8000'):
        self.server_ip = server_ip
        self.program_url = "http://" + server_ip
        self.ws_url = "ws://" + server_ip + '/scratch-ws/'
        self.program_name = ''
        self.controller_name = ''
        self.commands = []
        self.is_editing_program = False
        self.websocket = None
        self.ws_commands_to_send = []
        self.asyncio_loop = None
        self.should_keep_alive = True

    def keep_alive_forever(self):
        while self.should_keep_alive:
            pass

    def keep_alive_until_done(self):
        while len(self.ws_commands_to_send) > 0:
            pass
        self.should_keep_alive = False

    def connect(self, name):
        self.controller_name = name
        self.setup_websocket()

    def setup_websocket(self):
        thread = Thread(target=self.start_ws_loop, args=())
        thread.daemon = True
        thread.start()

    def start_ws_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.ensure_future(self.websocket_loop(),
                                       loop=loop)
        loop.run_until_complete(future)

    async def websocket_loop(self):
        self.ws = connect(self.ws_url)
        try:
            self.ws.recv()
            self.ws.send(json.dumps({
                'type': 'change-name',
                'name': self.controller_name
            }))
        except websockets.ConnectionClosedOK:
            print("Websocket closed!")
            return

        while self.should_keep_alive:
            if (len(self.ws_commands_to_send) > 0):
                command = self.ws_commands_to_send[0]
                args = None
                try:
                    args = command['Args']
                except KeyError:
                    args = ''

                self.ws.send(json.dumps({
                    'type': 'command',
                    'Command': command['Command'],
                    'Args': args
                }))
                self.ws_commands_to_send.pop(0)

    def send_program(self):
        self.is_editing_program = False
        try:
            response = requests.post(self.program_url + "/program", data=json.dumps(
                {'name': self.program_name, 'commands': self.commands}))
            is_valid = response.json()['valid']
            return is_valid
        except Exception as e:
            print(f'Error sending program: {e}')

    '''
    Sends a command to the server containing the command information using a post request
    '''

    def _add_program_command(self, command_info):
        if self.is_editing_program:
            self.commands.append(command_info)

    def _send_command(self, command_info):
        if self.is_editing_program:
            self._add_program_command(command_info)
        else:
            self.ws_commands_to_send.append(command_info)

    '''
    Signifies the start of a command chunk and allows commands to be added
    '''

    def start_program(self, program_name):
        self.is_editing_program = True
        self.program_name = program_name

    '''
    Tells Spot to stand
    '''

    def stand(self):
        command_info = {
            'Command': 'stand'
        }
        self._send_command(command_info)
        if not self.is_editing_program:
            time.sleep(2)

    '''
    Tells Spot to sit
    '''

    def sit(self):
        command_info = {
            'Command': 'sit'
        }
        self._send_command(command_info)
        if not self.is_editing_program:
            time.sleep(2)

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
        self._send_command(command_info)
        if not self.is_editing_program:
            time.sleep(0.1)

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
        self._send_command(command_info)
        if not self.is_editing_program:
            time.sleep(1)

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
        self._send_command(command_info)

    def send_file(self, path, type="file", main_filename="main.py"):
        import os
        import requests
        files = {}
        data = {
            "main": main_filename
        }
        assert main_filename.endswith(
            ".py"), "Wrong filetype for main_filename! (needs .py)"
        if type == "file":
            assert path.endswith(".py"), "Wrong Filetype! (needs .py)"
            assert os.path.exists(path), "File does not exist!"
            files = {'file': open(path, 'rb')}
            data = {'folder': False}
        elif type == "folder":
            assert os.path.exists(path), "Directory does not exist!"
            for file in os.listdir(path):
                files[file] = open(path + "\\" + file, 'rb')

        response = requests.post(
            self.program_url + "/file", files=files, data=data)
        is_valid = response.json()['valid']
        return is_valid
