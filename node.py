import sys

from dependencies import *


def can_mesg_tx(can_id, msg):
    # Send CAN message
    message = f"{can_id}::{msg}"
    s.send(message.encode())
    return True


def can_mesg_rx():
    # Receive CAN message

    with open("bus.txt", "r") as f:
        last_line = f.readlines()[-1]
    return last_line


def random_bits():
    return random.randint(0, 1)


def send_message(msg):
    can_id = node.get_ID()
    return can_mesg_tx(can_id, msg)


max_len = 50


class ECU:
    def __init__(self, node_id):
        self.node_id = node_id
        self.keep_track = {}
        self.primary = -1
        self.finished = False
        self.n = max_len
        self.acceptable = 2
        self.status = 0
        self.fa = 0
        self.mypair = []
        self.y = []
        self.z = []
        self.secret = []
        self.mypair = []
        self.sender = False
        self.leader = -1

    def store_random_bits(self, iter, bits):
        self.keep_track[iter] = bits

    def print_random_bits(self):
        print(self.keep_track)

    def return_info(self):
        return self.keep_track

    def get_ID(self):
        return self.node_id

    def find_secret(self):
        G = []
        enum = 0
        for i, j in zip(self.y, self.z):
            if i == j == 0:
                G.append(enum)
            enum += 1
        print("Inside Secret HERE\t\n", self.y, self.z)
        print(G)
        if self.primary:
            self.secret = self.fa[G]
        else:
            self.secret = 1 - self.fa[G]
        if self.secret.shape[0] > self.acceptable:
            self.finished = True
        else:
            self.status = 0
            self.finished = False

        print(
            "Finished Secret Finding\t",
            self.secret,
            self.secret.shape,
        )

    def set_primary(self, primary):
        self.primary = primary

    def set_keylength(self, n):
        self.sa = [False] * n

    def is_finished(self):
        return self.finished

    def print(self):
        s = f"ECU {self.node_id}:\n"
        s += f"Primary: {self.primary}\n"
        s += f"Finished: {self.finished}\n"
        s += f"Secret: {self.secret}\n"
        s += f"MyPair: {self.mypair}\n"
        s += f"Status: {self.status}\n"
        s += f"Sender: {self.sender}\n"
        s += f"Leader: {self.leader}\n"

        s += f"y: {self.y}\n"
        s += f"z: {self.z}\n"
        s += f"fa: {self.fa}\n"

        print(s)


nodes = 10


tick = 200
node_id = int(sys.argv[1])
node = ECU(node_id)
# log = open(f"log/{node_id}.txt", "w")
# sys.stdout = log

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print(node_id, sys.argv)


def speed():
    threading.Timer(1, speed).start()
    global tick
    stime = gettime() % 10
    print(gettime(), stime, node.print())
    if stime < 5:
        tick += 1
        last_line = can_mesg_rx()
        print(last_line, node_id)
        cans = last_line.strip().split("::")[0].split(",")
        cans = list(map(int, cans))
        print("CANS", cans)

        if "pair" in last_line:
            print("pairing happening")
            nodes_pairing = last_line.strip().split("_")[1].split(",")
            nodes_pairing = list(map(int, nodes_pairing))
            print(nodes_pairing)
            if node_id in nodes_pairing:
                node.sender = True
                if node.is_finished():
                    nodes_sorted = ",".join(str(v) for v in sorted(node.mypair))
                    send_message(f"Paired{nodes_sorted}")
                    return
                print("My turn)")
                if node_id == nodes_pairing[0]:
                    node.primary = True
                    stime = 0.1
                else:
                    node.primary = False
                    stime = 0.9

                n = nodes_pairing[2]
                if node.status == 0:
                    node.status = 1
                    node.acceptable = int(n)
                    nums = np.random.choice([0, 1], size=max_len).transpose()
                    node.fa = nums
                    print(nums)

                    node.mypair = [nodes_pairing[0], nodes_pairing[1]]
                    time.sleep(stime)
                    send_message(",".join(str(v) for v in nums))
                    # time.sleep(5)

        if "virtual" in last_line:
            print("virtual pairing happening")
            nodes_pairing = last_line.strip().split("_")[1].split(",")
            print(nodes_pairing)
            primary = nodes_pairing[0].split(".")
            secondary = nodes_pairing[1].split(".")
            primary = list(map(int, primary))
            secondary = list(map(int, secondary))
            print(primary, secondary)
            if node.status == 4:
                node.status = 0

            if node_id in primary or node_id in secondary:

                if node_id == primary[0] or node_id == secondary[0]:
                    node.sender = True
                else:
                    node.sender = False
                    if (
                        node.status == 0
                        and node.leader != primary[0]
                        and node.leader != secondary[0]
                    ):
                        bits = np.array([-1] * node.fa.shape[0])
                        for a1 in range(node.fa.shape[0]):
                            if node.fa[a1] == 1 and node.y[a1] == 1:
                                bits[a1] = 1

                            elif node.fa[a1] == 1 and node.y[a1] == 0:
                                bits[a1] = 0
                        reversefa = 1 - node.fa
                        for a1 in range(reversefa.shape[0]):
                            if reversefa[a1] == 1 and node.z[a1] == 1:
                                bits[a1] = 0

                            elif reversefa[a1] == 1 and node.z[a1] == 0:
                                bits[a1] = 1
                        print("BITS", bits)
                        node.fa = bits
                        if node_id in primary:
                            node.leader = primary[0]
                        else:
                            node.leader = secondary[0]

                node.status = 1
                node.acceptable = int(nodes_pairing[2])
                if node_id in primary:
                    node.primary = True
                    stime = 0.1
                else:
                    node.primary = False
                    stime = 0.9
                node.mypair = [primary[0], secondary[0]]
                time.sleep(stime)
                if node.sender:
                    send_message(",".join(str(v) for v in node.fa))
                time.sleep(5)
                print(nodes_pairing)

            print(nodes_pairing)

        if node.status == 1 and node.mypair == cans:
            print("I am here")
            print("Cur_message ")
            y = gety(last_line)

            node.y = y
            if node.status == 1:
                node.status = 2
                nums = 1 - node.fa
                print(nums)
                time.sleep(stime)
                if node.sender:
                    send_message(",".join(str(v) for v in nums))
                time.sleep(5)
        if node.status == 2 and node.mypair == cans:
            y = gety(last_line)
            print(node.y, y)
            if (node.y == y).all():
                print("ignore")
            else:

                node.z = y
                node.status = 3
                print("Trying to find secret")
                node.find_secret()
                nodes_sorted = ",".join(str(v) for v in sorted(node.mypair))
                if node.is_finished():
                    print("Finished")
                    node.status = 4
                    if node.sender:
                        send_message(f"Paired{nodes_sorted}")
                else:
                    node.status = 0
                    if node.sender:

                        send_message(f"Failed{nodes_sorted}")


speed()
