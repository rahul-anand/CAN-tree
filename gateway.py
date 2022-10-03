## Translated to a reacl single ECU, no shared state


# phases: Arbitration, Data Phase

import sys
from gc import is_finalized

from dependencies import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


def send_message(msg):
    message = f"{-1}::{msg}"
    s.send(message.encode())

    return True


def speed():

    threading.Timer(5, speed).start()
    global nodes, number, flag, messages
    stime = gettime() % 10
    print(gettime(), stime, flag)

    with open("bus.txt", "r") as f:

        last_line = f.readlines()[-1]
    print(last_line, node_id)
    if flag == 1:
        print("Sending Messages", messages, flag)
        if len(messages) > 0:
            send_message(messages[0])
        flag = 0
    elif "Paired" in last_line:
        flag = 1
        del messages[0]

    elif "Failed" in last_line:
        flag = 1


node_id = -1


length = 30

node_num = 8
nodes = [i for i in range(node_num)]

messages = []

iter = 1
while iter <= len(nodes):

    start = 0
    end = len(nodes)

    while start + iter <= end:
        cur_interval = nodes[start : start + iter]
        print(cur_interval)
        if iter == 2:
            messages.append(f"pair_{cur_interval[0]},{cur_interval[1]},{length}")
        if iter > 2:
            print("Interval:", cur_interval)
            mid_point = len(cur_interval) // 2

            first_half = ".".join(str(v) for v in cur_interval[0:mid_point])
            print(first_half)

            second_half = ".".join(str(v) for v in cur_interval[mid_point:])
            print(second_half)
            messages.append(f"virtual_{first_half},{second_half},{length}")

        start += iter
    iter *= 2
print(messages)


number = 0
flag = 1
speed()
