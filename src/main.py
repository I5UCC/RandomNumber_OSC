from pythonosc import udp_client
import json
import os
import sys
import random
from threading import Timer
import argparse
import openvr

class RepeatedTimer(object):
	def __init__(self, interval: float, function, *args, **kwargs):
		self._timer: Timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running: bool = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False


def get_absolute_path(relative_path):
    """Gets absolute path from relative path"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def cls():
    """Clears Console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def send_osc_message(parameter, value):
    oscClient.send_message("/avatar/parameters/" + parameter, value)

def get_random(type, min, max):
    match type:
        case "int":
            return random.randint(min, max)
        case "float":
            return round(random.uniform(min, max), 4)
        case "bool":
            return random.choice([True, False])
        
    return None

def send_parameter(param, index):
    value = get_random(param["Type"], param["Min"], param["Max"])
    name = param["Name"]
    output[index] = name + ": \t" + str(value)
    send_osc_message(name, value)

def print_output(output):
    cls()
    for line in output:
        print(line)


# Argument Parser
parser = argparse.ArgumentParser(description='RandomNumber_OSC: Sends random numbers via OSC')
parser.add_argument('-d', '--debug', required=False, action='store_true', help='prints values for debugging')
parser.add_argument('-i', '--ip', required=False, type=str, help="set OSC ip. Default=127.0.0.1")
parser.add_argument('-p', '--port', required=False, type=str, help="set OSC port. Default=9000")
args = parser.parse_args()

config_path = get_absolute_path('config.json')
manifest_path = get_absolute_path('app.vrmanifest')
config = json.load(open(config_path, "r"))
IP = args.ip if args.ip else config["IP"]
PORT = args.port if args.port else config["Port"]
oscClient = udp_client.SimpleUDPClient(IP, PORT)
application = openvr.init(openvr.VRApplication_Utility)
openvr.VRApplications().addApplicationManifest(manifest_path)

print("RandomNumber_OSC running...\n")
print("You can minimize this window.\n")
print("Press CTRL+C to exit.\n")
print(f"IP:\t\t\t{IP}")
print(f"Port:\t\t\t{PORT}")
print("\n---------------Parameters---------------\n")
for param in config["Parameters"]:
    print(f"{param['Name']}:\t\t{param['Min']} - {param['Max']} ({param['Type']}) - {param['Interval']}s")

output = []
i = 0
for param in config["Parameters"]:
    output.append(param["Name"])
    RepeatedTimer(param["Interval"], send_parameter, param, i).start()
    i += 1

if args.debug:
    lowest_interval = min([param["Interval"] for param in config["Parameters"]])
    RepeatedTimer(lowest_interval, print_output, output).start()