### Pregunta 2 (5 puntos): Crea un sistema de coordinación de tareas en una red de robots industriales:

- Usa el algoritmo de Chandy-Lamport para tomar instantáneas del estado global de los robots durante la ejecución de n tareas.
- Implementa el algoritmo de Raymond para la exclusión mutua en el acceso a recursos compartidos entre los robots.
- Utiliza relojes vectoriales para asegurar el ordenamiento parcial de los eventos y detectar violaciones de causalidad.
- Integra un recolector de basura generacional para la gestión eficiente de la memoria en los nodos de control de los robots.

Para crear un sistema de coordinación de tareas en una red de robots industriales que incluya los requisitos mencionados, se deben implementar varias funcionalidades avanzadas. como las siguientes

### 1. Algoritmo de Chandy-Lamport para tomar instantáneas del estado global

El algoritmo de Chandy-Lamport toma una instantánea global de un sistema distribuido asíncrono. En este, usaremos `asyncio` para simular la ejecución concurrente de tareas en diferentes robots.

### 2. Algoritmo de Raymond para la exclusión mutua

El algoritmo de Raymond es un protocolo de exclusión mutua distribuido que asegura acceso seguro a recursos compartidos en una red de nodos.

### 3. Relojes Vectoriales

Los relojes vectoriales se utilizan para ordenar eventos y detectar violaciones de causalidad.

### 4. Recolector de Basura Generacional

Implementaremos un recolector de basura generacional básico para la gestión de memoria en los nodos de control.

A continuación, prsento el codigo:

```python
import asyncio
import logging
from collections import defaultdict, deque

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definición de clases y estructuras
class Robot:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.tasks = deque()
        self.snapshot = {}
        self.vector_clock = defaultdict(int)
        self.queue = deque()
        self.token_holder = None

    async def add_task(self, task):
        self.tasks.append(task)
        self.vector_clock[self.robot_id] += 1
        logger.info(f"Robot {self.robot_id} añade tarea {task} a la cola.")

    async def execute_task(self):
        while True:
            if self.tasks:
                task = self.tasks.popleft()
                await asyncio.sleep(1)  # Simular ejecución de tarea
                logger.info(f"Robot {self.robot_id} ejecuta tarea {task}.")
            await asyncio.sleep(0.1)

    async def request_token(self):
        # Implementar el algoritmo de Raymond para solicitar el token
        pass

    async def take_snapshot(self):
        self.snapshot = {"tasks": list(self.tasks), "vector_clock": dict(self.vector_clock)}
        logger.info(f"Robot {self.robot_id} toma una instantánea: {self.snapshot}")

    async def manage_memory(self):
        # Implementar un recolector de basura generacional básico
        pass

class Network:
    def __init__(self, num_robots):
        self.robots = [Robot(robot_id) for robot_id in range(num_robots)]
        self.token_holder = 0

    async def distribute_tasks(self, tasks):
        for i, task in enumerate(tasks):
            await self.robots[i % len(self.robots)].add_task(task)

    async def run(self):
        tasks = [robot.execute_task() for robot in self.robots]
        await asyncio.gather(*tasks)

# Simulación de la red de robots
async def main():
    network = Network(num_robots=3)
    tasks = ["Tarea1", "Tarea2", "Tarea3", "Tarea4", "Tarea5"]
    await network.distribute_tasks(tasks)
    await network.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Explicación del Código:

1. **Clase `Robot`:**
   - Cada robot tiene una cola de tareas (`tasks`), un vector de reloj (`vector_clock`) y un mecanismo para almacenar instantáneas (`snapshot`).
   - La función `add_task` añade tareas a la cola y actualiza el reloj vectorial.
   - La función `execute_task` ejecuta las tareas de la cola de manera asíncrona.

2. **Clase `Network`:**
   - Esta clase gestiona una red de robots y distribuye tareas entre ellos.
   - La función `distribute_tasks` asigna tareas a los robots de manera equitativa.

3. **Simulación:**
   - La función `main` crea una red de robots, distribuye tareas y ejecuta las tareas de manera concurrente.

### Implementaciones Adicionales:

1. **Algoritmo de Raymond para la Exclusión Mutua:**
   - Se debe implementar el método `request_token` en la clase `Robot` para manejar la solicitud y concesión del token.

2. **Algoritmo de Chandy-Lamport:**
   - El método `take_snapshot` en la clase `Robot` toma una instantánea del estado actual del robot.

3. **Relojes Vectoriales:**
   - Los relojes vectoriales se actualizan en cada operación relevante (`add_task`).

4. **Recolector de Basura Generacional:**
   - El método `manage_memory` en la clase `Robot` manejaría la recolección de basura generacional.


### Resultado:

![alt text](<Captura desde 2024-07-12 16-29-44.png>)