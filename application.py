## Translated to a reacl single ECU, no shared state


# phases: Arbitration, Data Phase

from gc import is_finalized

from dependencies import *


def can_mesg_tx(can_id, payload):
    # Send CAN message
    pass


def can_mesg_rx(can_id, payload):
    # Receive CAN message
    pass


def receive():
    # Receive CAN message
    pass


# tick = 200


# def speed():
#     threading.Timer(1, speed).start()
#     global tick
#     tick += 1
#     print(tick)


# speed()


class simulator:
    def __init__(self):
        self.bus = {}
        self.timer = 0
        self.bus[self.timer] = 0

    # def


def random_bits():
    return random.randint(0, 1)


class ECU:
    def __init__(self, node_id):
        self.node_id = node_id
        self.keep_track = {}
        self.primary = -1
        self.finished = False
        self.n = 10

    def store_random_bits(self, iter, bits):
        self.keep_track[iter] = bits

    # def store_observed(self, iter, bits):
    #     self.keep_track[iter] = bits

    def print_random_bits(self):
        print(self.keep_track)

    def return_info(self):
        return self.keep_track

    def find_secret(self):

        y = self.keep_track[f"observed{0}"]
        z = self.keep_track[f"observed{1}"]
        G = []
        enum = 0
        for i, j in zip(y, z):
            if i == j == 0:
                G.append(enum)
            enum += 1
            # else:
            #     G.append(random_bits())
        print("HERE\t\n", y, z)
        print(G)
        if self.primary:
            self.secret_key = self.keep_track[f"rand{0}"][G]
        else:
            self.secret_key = 1 - self.keep_track[f"rand{0}"][G]
        if self.secret_key.shape[0] > self.n:
            self.finished = True

        print(
            "Finished\t",
            # self.keep_track,
            # "\n",
            # self.primary,
            self.secret_key,
            self.secret_key.shape,
        )

    def set_primary(self, primary):
        self.primary = primary

    def set_keylength(self, n):
        self.sa = [False] * n

    def is_finished(self):
        return self.finished


def Gateway():
    def __init__(
        self,
    ):
        self.nodes = []

    # def __init__(self, node_id):
    # pass


nodes = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
# Discovery Phase
node_dict = {}
for i in range(nodes):
    node = ECU(i)
    # node.ctime()
    node_dict[i] = node

    final_message = f"{i}::discovery"
    # node_dict[i].store_random_bits(f"rand{iter}", nums)
    s.send(final_message.encode())
    time.sleep(1)


print(node_dict)


epoch_time = gettime()
print(epoch_time)
# sequence = []


# s.send("ed".encode())


pairs = [1, 2]

primaries = {}

primaries[1] = True
primaries[2] = False
n = 20

for i in pairs:
    node_dict[i].set_primary(primaries[i])
    node_dict[i].set_keylength(n)

while True:

    for iter in range(2):
        for i in pairs:
            can_id = f"0x{i}"
            if iter == 0:
                nums = np.random.choice([0, 1], size=n).transpose()
            else:
                nums = 1 - node_dict[i].return_info()[f"rand{0}"]
            print(can_id, nums)
            final_message = f"{can_id}::{','.join(str(v) for v in nums)}"
            node_dict[i].store_random_bits(f"rand{iter}", nums)
            s.send(final_message.encode())
            time.sleep(0.5)

        for i in pairs:
            print(node_dict[i].print_random_bits())
            s.send("read".encode())

            y = s.recv(1024).decode()
            nums = np.array(ast.literal_eval(y))
            print(nums)
            node_dict[i].store_random_bits(f"observed{iter}", nums)

            print(y)
        # () + 1

        # break

    for i in pairs:

        print(node_dict[i].print_random_bits())

    for i in pairs:
        node_dict[i].find_secret()
    flag = 1

    for i in pairs:

        print(node_dict[i].is_finished())
        if node_dict[i].is_finished():
            continue
        else:
            flag = 0
    print("FLAG", flag)
    if flag:
        break
