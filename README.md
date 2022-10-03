1. Assuming all nodes are time-synchronized, written in Python and one time interval of 10 second. To simulate Bus I write to a file and last entry of bus denotes the current data. bus.txt is also the information that is accessible to a passive adversary.

2. To send messages to the simluator I use socket programming. BUS does logical AND of all data messages received in a time period, it also concates the CAN IDs in the final response.

3. Gateway.py contains the code running on gateway node that is orchestrating the nodes, bus and the simulator.

4. Assuming that the gateway node knows all active nodes.


To run

1. Run the simulator.py
2. To launch each node, run node.py node_ID in separate terminals
3. Launch gateway.py to  start the key-exchange process