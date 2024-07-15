import asyncio
import logging
import random
from collections import deque
from typing import Any, Callable, Dict, List

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Clase Message
class Message:
    def __init__(self, sender: int, content: Any, timestamp: int):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp

# Clase Process (Dijkstra-Scholten)
class Process:
    def __init__(self, process_id, neighbors):
        self.process_id = process_id
        self.neighbors = neighbors
        self.parent = None
        self.children = set()
        self.active = True

    def send_message(self, recipient):
        recipient.receive_message(self, self.process_id)

    def receive_message(self, sender, sender_id):
        if self.parent is None:
            self.parent = sender
        self.children.add(sender_id)
        self.process_task()

    def process_task(self):
        # Simular procesamiento de tarea
        self.active = False
        self.check_termination()

    def check_termination(self):
        if not self.active and not self.children:
            if self.parent:
                self.parent.receive_termination(self.process_id)

    def receive_termination(self, child_id):
        self.children.remove(child_id)
        self.check_termination()

# Clase RicartAgrawalaMutex
class RicartAgrawalaMutex:
    def __init__(self, node_id, num_nodes, nodes):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.nodes = nodes
        self.clock = 0
        self.request_queue = []
        self.replies_received = 0

    def request_access(self):
        self.clock += 1
        self.request_queue.append((self.clock, self.node_id))
        for node in self.nodes:
            if node.node_id != self.node_id:
                node.receive_request(self.clock, self.node_id)

    def receive_request(self, timestamp, sender_id):
        self.clock = max(self.clock, timestamp) + 1
        self.request_queue.append((timestamp, sender_id))
        self.request_queue.sort()
        self.send_reply(sender_id)

    def send_reply(self, target_id):
        for node in self.nodes:
            if node.node_id == target_id:
                node.receive_reply(self.node_id)

    def receive_reply(self, sender_id):
        self.replies_received += 1
        if self.replies_received == self.num_nodes - 1:
            self.enter_critical_section()

    def enter_critical_section(self):
        print(f"Nodo {self.node_id} ingresando a la sección crítica")
        # Código de la sección crítica aquí
        self.leave_critical_section()

    def leave_critical_section(self):
        self.replies_received = 0
        self.request_queue = [(t, n) for t, n in self.request_queue if n != self.node_id]
        for timestamp, node_id in self.request_queue:
            self.send_reply(node_id)
        print(f"Nodo {self.node_id} dejando la sección crítica")

# Clase BerkeleyNode y BerkeleyMaster para sincronización de relojes
class BerkeleyNode:
    def __init__(self, node_id, time):
        self.node_id = node_id
        self.time = time

    def adjust_time(self, offset):
        self.time += offset

class BerkeleyMaster:
    def __init__(self, nodes):
        self.nodes = nodes

    def synchronize_clocks(self):
        times = [node.time for node in self.nodes]
        average_time = sum(times) / len(times)
        for node in self.nodes:
            offset = average_time - node.time
            node.adjust_time(offset)
        return [(node.node_id, node.time) for node in self.nodes]

# Clase CheneyCollector para recolección de basura
class CheneyCollector:
    def __init__(self, size):
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.free_ptr = 0

    def allocate(self, obj):
        if self.free_ptr >= self.size:
            self.collect()
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        self.to_space = [None] * self.size
        self.free_ptr = 0
        for obj in self.from_space:
            if obj is not None:
                self.copy(obj)
        self.from_space, self.to_space = self.to_space, self.from_space

    def copy(self, obj):
        addr = self.free_ptr
        self.to_space[addr] = obj
        self.free_ptr += 1
        return addr

# Clase Network para coordinar los nodos
class Network:
    def __init__(self, num_nodes):
        self.nodes = []
        self.berkeley_nodes = [BerkeleyNode(i, random.randint(0, 100)) for i in range(num_nodes)]
        self.master = BerkeleyMaster(self.berkeley_nodes)
        self.collector = CheneyCollector(10)
        self.nodes = [RicartAgrawalaMutex(i, num_nodes, self.nodes) for i in range(num_nodes)]

    async def start(self):
        await asyncio.gather(self.run_ricart_agrawala(), self.run_berkeley())

    async def run_ricart_agrawala(self):
        for node in self.nodes:
            node.request_access()
            await asyncio.sleep(1)
            node.leave_critical_section()

    async def run_berkeley(self):
        synchronized_times = self.master.synchronize_clocks()
        print(f"Tiempos sincronizados: {synchronized_times}")

    def stop(self):
        print("Red detenida")

# Simulación de la red de computadoras
async def main():
    network = Network(num_nodes=3)
    await network.start()
    network.stop()

if __name__ == "__main__":
    asyncio.run(main())
