# Replicated-key-value-data-store
Replicated key-value data store with the help of ZooKeeper:
This project implements a replicated key-value data store maintained by multiple servers using ZooKeeper for leader election. Each server maintains a copy of the data store and exposes functions for reading and adding/updating key-value pairs. The leader server is responsible for handling write requests and propagating updates to other replicas.

     Installation
Install Docker on your machine by following the instructions here.
Pull the ZooKeeper image from Docker Hub:
Copy code
$ docker pull zookeeper
Usage
Start the ZooKeeper servers using Docker Swarm:
bash
Copy code
$ docker swarm init
$ docker stack deploy --compose-file docker-compose.yml zookeeper
Run the server program (server.py) on each server with the following command:
bash
Copy code
$ python server.py --host <hostip> --port <port> -zookeeper <zookeeper_ip> -zookeeper_port <zk_port>
Execute the test script (test_script.py) to verify the functionality of the replicated data store:
bash
Copy code
$ python test_script.py

          Test Cases
Test 1: Perform leader election to select a leader server.
Test 2: Add/update a key-value pair in the data store.
Test 3: Read the value associated with a key from the data store.
Test 4: Add/update the same key-value pair again to test updating functionality.
Test 5: Read the value of the key after updating to verify successful update.
Test 6: Perform leader re-election and observe the impact on data retrieval.

    Additional Notes
Ensure that ZooKeeper servers are running and properly configured before starting the server program.
Each server should have a unique ID for identification during leader election.
The test script covers basic functionality testing, but additional test cases can be added for comprehensive testing.
