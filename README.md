1. Assuming all nodes are time-synchronized, written in Python and one time interval of 10 seconds. To simulate Bus I write to a file and the last entry of BUS denotes the current data. bus.txt is also the information that is accessible to a passive adversary.

2. To send messages to the simulator I use socket programming. BUS does logical AND of all data messages received in a period, it also concantenates the CAN IDs in the final response.

3. Gateway.py contains the code running on the gateway node that is orchestrating the nodes, bus and the simulator.

4. Assuming that the gateway node knows all active nodes.

5. The length of random bits is denoted by max_len and set to 500.

6. The gateway node can specify the acceptable target length of a shared secret.

7. Socket is assumed to be of size 1024 and need to be modified to support large arrays.

7. Demo video demonstrating the key-exchange protocol for 8 nodes.

Libraries used: threading, time, socket 
To run

1. Run the simulator.py
2. To launch each node, run node.py node_ID in separate terminals
3. Launch gateway.py to  start the key-exchange process