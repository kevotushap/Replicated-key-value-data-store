import random
import threading
import time

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError


# Function to connect to ZooKeeper
def connect_zookeeper(hosts):
    zk = KazooClient(hosts=hosts)
    zk.start()
    return zk

# Function to verify ZooKeeper configuration
def verify_zookeeper_configuration(zk_hosts):
    try:
        hostname, port = zk_hosts.split(':')
        if not port.isdigit():
            print("Invalid port number in zk_hosts:", zk_hosts)
            return False
        return True
    except Exception as e:
        print("Error verifying ZooKeeper configuration:", e)
        return False

# Function to perform add/update operation
def add_update(zk, key, value):
    zk.ensure_path("/datastore")
    try:
        zk.set("/datastore/" + key, value.encode())
        print("Added/updated key:", key, "with value:", value)
    except Exception as e:
        print("An error occurred while setting data:", e)

# Function to perform read operation
def read(zk, key):
    try:
        data, _ = zk.get("/datastore/" + key)
        return data.decode()
    except Exception as e:
        print("An error occurred while reading data:", e)
        return None

# Function to simulate server behavior
def simulate_server(zk_hosts, server_id):
    zk = connect_zookeeper(zk_hosts)
    print("Server", server_id, "started and connected to ZooKeeper")

    # Simulate leader election
    def watch_leader_election(children):
        if children:  # Check if children is not empty
            leader = min(children)
            print("Server", server_id, "Leader elected:", leader)

    # Simulate add/update operation
    while True:
        key = "key" + str(random.randint(1, 10))
        value = "value" + str(random.randint(1, 100))
        add_update(zk, key, value)
        time.sleep(random.randint(1, 5))

# Function to simulate leader node failure
def simulate_leader_failure(zk_hosts):
    zk = connect_zookeeper(zk_hosts)
    print("Leader failure simulation started")

    while True:
        try:
            children = zk.get_children("/election")
            if children:
                leader = min(children)
                print("Killing leader:", leader)
                zk.delete("/election/" + leader)
                break
        except NoNodeError:
            pass
        except Exception as e:
            print("An error occurred:", e)
            break

# Function to simulate stale read scenario
def simulate_stale_read(zk_hosts):
    zk = connect_zookeeper(zk_hosts)
    print("Stale read simulation started")

    # Create /election node if it doesn't exist
    if not zk.exists("/election"):
        zk.create("/election", b"")

    # Wait for leader to be killed
    time.sleep(5)

    # Check if leader has recovered
    children = zk.get_children("/election")
    if children:
        leader = min(children)
        print("Leader recovered:", leader)

        # Wait for data to become stale
        time.sleep(100)

        # Perform read operation on the killed leader
        key = "key" + str(random.randint(1, 10))
        print("Performing stale read for key:", key)
        data = read(zk, key)
        print("Stale read result:", data)


if __name__ == "__main__":
    zk_hosts = "localhost:2181"
    zk = connect_zookeeper(zk_hosts)

    # Create /election node if it doesn't exist
    if not zk.exists("/election"):
        zk.create("/election", b"")

    threads = []

    # Start 3 servers
    for i in range(3):
        thread = threading.Thread(target=simulate_server, args=(zk_hosts, i + 1))
        threads.append(thread)
        thread.start()

    # Start leader failure simulation
    leader_failure_thread = threading.Thread(target=simulate_leader_failure, args=(zk_hosts,))
    leader_failure_thread.start()

    # Start stale read simulation
    stale_read_thread = threading.Thread(target=simulate_stale_read, args=(zk_hosts,))
    stale_read_thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    leader_failure_thread.join()
    stale_read_thread.join()

    # Function to set data
    def set_data(path, data):
        try:
            # Check if node exists before setting data
            if zk.exists(path):
                zk.set(path, data.encode())  # Encode data as bytes before setting
                print("Data set successfully at path:", path)
            else:
                print("Node does not exist:", path)
        except Exception as e:
            print("Error setting data:", e)

    # Example usage of set_data function
    set_data("/example_node", "example_data")

    # Stop ZooKeeper client
    zk.stop()
