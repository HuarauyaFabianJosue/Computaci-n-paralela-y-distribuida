import asyncio
import logging
import threading
from collections import defaultdict, deque

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Algoritmo de Raymond para la exclusión mutua
class RaymondMutex:
    def __init__(self, node_id, parent=None):
        self.node_id = node_id
        self.parent = parent
        self.token_holder = (parent is None)
        self.request_queue = []

    def request_access(self):
        if self.token_holder:
            self.enter_critical_section()
        else:
            self.request_queue.append(self.node_id)
            self.send_request_to_parent()

    def send_request_to_parent(self):
        if self.parent:
            self.parent.receive_request(self)

    def receive_request(self, requester):
        if not self.token_holder:
            self.request_queue.append(requester.node_id)
            self.send_request_to_parent()
        elif requester.node_id == self.node_id:
            self.enter_critical_section()
        else:
            self.send_token(requester)

    def send_token(self, requester):
        self.token_holder = False
        requester.receive_token(self)

    def receive_token(self, sender):
        self.token_holder = True
        if self.request_queue and self.request_queue[0] == self.node_id:
            self.enter_critical_section()
        else:
            self.send_token_to_next_in_queue()

    def send_token_to_next_in_queue(self):
        next_node_id = self.request_queue.pop(0)
        next_node = [node for node in nodes if node.node_id == next_node_id][0]
        self.send_token(next_node)

    def enter_critical_section(self):
        print(f"Nodo {self.node_id} ingresando a la sección crítica")
        # Código de la sección crítica aquí
        self.leave_critical_section()

    def leave_critical_section(self):
        print(f"Nodo {self.node_id} dejando la sección crítica")
        if self.request_queue:
            self.send_token_to_next_in_queue()

# Relojes vectoriales para el orden de eventos
class VectorClock:
    def __init__(self, node_ids):
        self.clock = {node_id: 0 for node_id in node_ids}

    def increment(self, node_id):
        self.clock[node_id] += 1

    def update(self, other_clock):
        for node_id in self.clock.keys():
            self.clock[node_id] = max(self.clock[node_id], other_clock[node_id])

    def get_clock(self):
        return self.clock

# Recolector de basura generacional
class GenerationalGarbageCollector:
    def __init__(self):
        self.generations = {0: [], 1: [], 2: []}

    def allocate(self, obj):
        self.generations[0].append(obj)

    def collect(self):
        for gen in range(2, -1, -1):
            for obj in self.generations[gen]:
                if not obj.is_alive():
                    self.generations[gen].remove(obj)
            if gen < 2:
                self.generations[gen + 1].extend(self.generations[gen])
                self.generations[gen] = []

class Object:
    def __init__(self):
        self.alive = True

    def is_alive(self):
        return self.alive

# Algoritmo de Chandy-Lamport para instantáneas
class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.state = None
        self.channels = defaultdict(list)
        self.neighbors = []
        self.marker_received = {}
        self.local_snapshot = None
        self.lock = threading.Lock()

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in neighbors:
            self.marker_received[neighbor.process_id] = False

    def initiate_snapshot(self):
        with self.lock:
            self.local_snapshot = self.state
            print(f"Process {self.process_id} taking local snapshot: {self.local_snapshot}")
            self.send_marker_messages()

    def send_marker_messages(self):
        for neighbor in self.neighbors:
            self.send_message(neighbor, 'MARKER')

    def send_message(self, neighbor, message_type, content=None):
        message = (message_type, self.process_id, content)
        neighbor.receive_message(message)

    def receive_message(self, message):
        message_type, sender_id, content = message
        with self.lock:
            if message_type == 'MARKER':
                if not self.marker_received[sender_id]:
                    self.marker_received[sender_id] = True
                    if self.local_snapshot is None:
                        self.local_snapshot = self.state
                        print(f"Process {self.process_id} taking local snapshot: {self.local_snapshot}")
                        self.send_marker_messages()
                    else:
                        self.channels[sender_id].append(content)
                else:
                    self.channels[sender_id].append(content)
            else:
                if self.local_snapshot is not None:
                    self.channels[sender_id].append(content)
                else:
                    self.process_message(message)

    def process_message(self, message):
        print(f"Process {self.process_id} received message from Process {message[1]}: {message[2]}")

    def update_state(self, new_state):
        self.state = new_state

# Clase Robot con todas las funcionalidades
class Robot:
    def __init__(self, robot_id, parent=None):
        self.robot_id = robot_id
        self.tasks = deque()
        self.snapshot = {}
        self.vector_clock = VectorClock([robot_id])
        self.mutex = RaymondMutex(robot_id, parent)
        self.memory = []
        self.state = None
        self.channels = defaultdict(list)
        self.neighbors = []
        self.marker_received = {}
        self.local_snapshot = None
        self.lock = threading.Lock()

    async def add_task(self, task):
        self.tasks.append(task)
        self.vector_clock.increment(self.robot_id)
        logger.info(f"Robot {self.robot_id} añade tarea {task} a la cola.")

    async def execute_task(self):
        while True:
            if self.tasks:
                task = self.tasks.popleft()
                await asyncio.sleep(1)  # Simular ejecución de tarea
                logger.info(f"Robot {self.robot_id} ejecuta tarea {task}.")
            await asyncio.sleep(0.1)

    async def request_token(self):
        self.mutex.request_access()

    async def take_snapshot(self):
        self.snapshot = {"tasks": list(self.tasks), "vector_clock": self.vector_clock.get_clock()}
        logger.info(f"Robot {self.robot_id} toma una instantánea: {self.snapshot}")

    async def manage_memory(self):
        self.memory = [item for item in self.memory if not self.is_garbage(item)]
        logger.info(f"Robot {self.robot_id} gestionó la memoria.")

    def is_garbage(self, item):
        return False

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in neighbors:
            self.marker_received[neighbor.robot_id] = False

    def initiate_snapshot(self):
        with self.lock:
            self.local_snapshot = self.state
            print(f"Robot {self.robot_id} taking local snapshot: {self.local_snapshot}")
            self.send_marker_messages()

    def send_marker_messages(self):
        for neighbor in self.neighbors:
            self.send_message(neighbor, 'MARKER')

    def send_message(self, neighbor, message_type, content=None):
        message = (message_type, self.robot_id, content)
        neighbor.receive_message(message)

    def receive_message(self, message):
        message_type, sender_id, content = message
        with self.lock:
            if message_type == 'MARKER':
                if not self.marker_received[sender_id]:
                    self.marker_received[sender_id] = True
                    if self.local_snapshot is None:
                        self.local_snapshot = self.state
                        print(f"Robot {self.robot_id} taking local snapshot: {self.local_snapshot}")
                        self.send_marker_messages()
                    else:
                        self.channels[sender_id].append(content)
                else:
                    self.channels[sender_id].append(content)
            else:
                if self.local_snapshot is not None:
                    self.channels[sender_id].append(content)
                else:
                    self.process_message(message)

    def process_message(self, message):
        print(f"Robot {self.robot_id} received message from Robot {message[1]}: {message[2]}")

    def update_state(self, new_state):
        self.state = new_state

# Clase Network con integración de todas las funcionalidades
class Network:
    def __init__(self, num_robots):
        self.robots = [Robot(robot_id) for robot_id in range(num_robots)]
        self.token_holder = 0

        # Establecer vecinos para cada robot para Chandy-Lamport
        for i, robot in enumerate(self.robots):
            neighbors = [self.robots[j] for j in range(num_robots) if i != j]
            robot.set_neighbors(neighbors)

    async def distribute_tasks(self, tasks):
        for i, task in enumerate(tasks):
            await self.robots[i % len(self.robots)].add_task(task)

    async def run(self):
        tasks = [robot.execute_task() for robot in self.robots]
        await asyncio.gather(*tasks)

    async def take_global_snapshot(self):
        for robot in self.robots:
            await robot.take_snapshot()
        logger.info("Snapshot global tomado.")

# Simulación de la red de robots
async def main():
    network = Network(num_robots=3)
    tasks = ["Tarea1", "Tarea2", "Tarea3", "Tarea4", "Tarea5"]
    await network.distribute_tasks(tasks)
    await asyncio.sleep(1)  # Simular un poco de tiempo antes de tomar la instantánea
    await network.take_global_snapshot()
    await network.run()

if __name__ == "__main__":
    asyncio.run(main())
