import ast
import os
import random
import sys
import threading
import time
from time import sleep

import numpy as np


def gettime():
    return int(time.time())


import socket
from threading import *


def split_message(message):
    print(message)
    splitted_message = message.split("::")
    can_id = splitted_message[0]
    only_message = splitted_message[1]
    return can_id, only_message


def gety(last_line):
    return np.array(list(ast.literal_eval(last_line.strip().split("::")[1])))


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8000
print(host)
print(port)
