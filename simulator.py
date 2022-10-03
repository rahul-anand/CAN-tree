from dependencies import *


class simulator:
    def __init__(self):
        self.bus = {}
        self.timer = 0
        self.bus[self.timer] = 0

    def receive(self, time, message):
        self.bus[time] = message

    def send(self, time):
        return self.bus[time]


stime = gettime()

etime = stime + 100

serversocket.bind((host, port))

busfile = open("bus.txt", "w")
busfile.writelines("Started\n")
busfile.flush()
os.fsync(busfile.fileno())


canbus = []

buffer = []


tick = 1


def clearbuffer():
    threading.Timer(1, clearbuffer).start()
    global tick, buffer
    stime = gettime() % 10
    print(buffer, gettime(), stime)
    buffer = list(set(buffer))
    if stime > 8:

        tick += 1
        if len(buffer) == 0:
            msg = "0::Nothing"
        elif len(buffer) == 1:
            msg = buffer[0]
        else:
            try:
                msg = "Something big"
                d1 = {}
                length = -1
                for message in buffer:
                    if "Failed" in message or "Paired" in message:
                        busfile.write(message + "\n")
                        busfile.flush()
                        print(stime)
                        buffer = []
                        os.fsync(busfile.fileno())
                        return
                    can_id, only_message = split_message(message)
                    x1 = ast.literal_eval(only_message)

                    d1[can_id] = np.array(list(x1))
                    length = len(x1)
                print(d1)
                cans = []
                ans = np.array([1] * length)
                for k1, v1 in sorted(d1.items()):
                    ans = ans & v1
                    cans.append(k1)
                print(ans)
                y = f"{','.join(str(v) for v in ans)}"
                msg = f"{','.join(str(v) for v in cans)}" + "::" + y
            except:
                msg = "Nothing"
                buffer = []
        busfile.write(msg + "\n")
        busfile.flush()
        print(stime)
        buffer = []
        os.fsync(busfile.fileno())


clearbuffer()


class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.data = {}
        self.nodes_available = []

        global canbus, busfile, buffer
        self.busfile = busfile

        self.start()

    def run(self):
        global canbus, buffer
        while 1:
            message = self.sock.recv(1024).decode()

            if "discovery" or "pair" in message:
                can_id, only_message = split_message(message)

                buffer.append(message)
                buffer = list(set(buffer))

                print(message)
            else:
                if len(message) != 0:
                    print("Client sent:", message, len(message))

                    only_message = message.split("::")[1]
                    print(only_message)
                    x1 = ast.literal_eval(only_message)
                    canbus.append(x1)

                time.sleep(1)

            print("CanBus", gettime(), canbus, "\n\n")


serversocket.listen(5)
print("server started and listening")
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
