import asyncio
import random
import time
from typing import List, Dict, Tuple

class Node:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.term = 0
        self.voted_for = None
        self.state = "follower"
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.votes_received = 0
        self.election_timeout = random.uniform(150, 300) / 1000

    async def start_election(self):
        self.state = "candidate"
        self.term += 1
        self.voted_for = self.node_id
        self.votes_received = 1
        print(f"Node {self.node_id} starts election for term {self.term}")

        for peer in self.network.nodes:
            if peer.node_id != self.node_id:
                await peer.request_vote(self.node_id, self.term)

        await asyncio.sleep(self.election_timeout)
        if self.votes_received > len(self.network.nodes) / 2:
            self.state = "leader"
            print(f"Node {self.node_id} becomes leader for term {self.term}")
            asyncio.create_task(self.send_heartbeats())
        else:
            self.state = "follower"

    async def request_vote(self, candidate_id, term):
        if term > self.term:
            self.term = term
            self.voted_for = candidate_id
            self.state = "follower"
            self.votes_received += 1
            print(f"Node {self.node_id} voted for {candidate_id} in term {self.term}")
            return True
        return False

    async def send_heartbeats(self):
        while self.state == "leader":
            for peer in self.network.nodes:
                if peer.node_id != self.node_id:
                    await peer.receive_heartbeat(self.node_id, self.term)
            await asyncio.sleep(1)

    async def receive_heartbeat(self, leader_id, term):
        if term >= self.term:
            self.term = term
            self.state = "follower"
            print(f"Node {self.node_id} received heartbeat from {leader_id} for term {self.term}")

    def crash(self):
        self.state = "crashed"
        print(f"Node {self.node_id} crashed")

    def recover(self):
        self.state = "follower"
        self.term += 1
        print(f"Node {self.node_id} recovered and rejoining election")

class Network:
    def __init__(self, num_nodes):
        self.nodes = [Node(i, self) for i in range(num_nodes)]
        self.latency = {}

    def partition(self, partition1: List[int], partition2: List[int]):
        for node in self.nodes:
            if node.node_id in partition1:
                node.peers = [n for n in self.nodes if n.node_id in partition1]
            elif node.node_id in partition2:
                node.peers = [n for n in self.nodes if n.node_id in partition2]

    def heal(self):
        for node in self.nodes:
            node.peers = [n for n in self.nodes if n.node_id != node.node_id]

    async def run_simulation(self):
        while True:
            node = random.choice(self.nodes)
            if node.state != "crashed":
                await node.start_election()
            await asyncio.sleep(random.uniform(1, 5))

    def simulate_latency(self, node1_id, node2_id, latency):
        self.latency[(node1_id, node2_id)] = latency

async def main():
    network = Network(num_nodes=5)

    # Simulate latency
    network.simulate_latency(0, 1, 0.1)
    network.simulate_latency(1, 2, 0.1)
    network.simulate_latency(2, 3, 0.1)
    network.simulate_latency(3, 4, 0.1)

    # Partition the network
    network.partition([0, 1], [2, 3, 4])
    await asyncio.sleep(5)
    network.heal()

    # Simulate node crashes and recoveries
    network.nodes[2].crash()
    await asyncio.sleep(3)
    network.nodes[2].recover()

    # Run the simulation
    await network.run_simulation()

if __name__ == "__main__":
    asyncio.run(main())