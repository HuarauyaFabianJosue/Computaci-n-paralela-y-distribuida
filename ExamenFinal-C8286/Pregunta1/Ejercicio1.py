import asyncio
import logging
import random
from collections import deque
from enum import Enum
from typing import Any, Callable, Deque, Dict

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definición de tipos de eventos
class EventType(Enum):
    EXECUTE_CELL = 1
    SAVE_NOTEBOOK = 2
    ADD_CELL = 3
    REMOVE_CELL = 4

class Event:
    def __init__(self, event_type: EventType, data: Any):
        self.event_type = event_type
        self.data = data

class Notebook:
    def __init__(self):
        self.cells = []
        self.lock = asyncio.Lock()

    async def add_cell(self, content: str):
        async with self.lock:
            self.cells.append(content)
            logger.info("Celda añadida: %s", content)

    async def remove_cell(self, index: int):
        async with self.lock:
            if 0 <= index < len(self.cells):
                removed = self.cells.pop(index)
                logger.info("Celda eliminada: %s", removed)
            else:
                logger.error("Índice fuera de rango: %d", index)

    async def execute_cell(self, index: int):
        async with self.lock:
            if 0 <= index < len(self.cells):
                # Simular ejecución de celda
                logger.info("Ejecutando celda %d: %s", index, self.cells[index])
                await asyncio.sleep(random.uniform(0.1, 0.5))  # Simular tiempo de ejecución
                logger.info("Ejecución completada: %s", self.cells[index])
            else:
                logger.error("Índice fuera de rango: %d", index)

    async def save_notebook(self):
        async with self.lock:
            # Simular guardado de notebook
            logger.info("Guardando notebook con %d celdas", len(self.cells))
            await asyncio.sleep(0.2)
            logger.info("Notebook guardado")

class EventLoop:
    def __init__(self):
        self.event_queue: Deque[Event] = deque()
        self.notebook = Notebook()
        self.event_handlers: Dict[EventType, Callable[[Any], Any]] = {
            EventType.EXECUTE_CELL: self.notebook.execute_cell,
            EventType.SAVE_NOTEBOOK: lambda _: self.notebook.save_notebook(),
            EventType.ADD_CELL: self.notebook.add_cell,
            EventType.REMOVE_CELL: self.notebook.remove_cell,
        }

    async def event_producer(self):
        # Simular eventos generados por el usuario
        events = [
            Event(EventType.ADD_CELL, "print('Hola mundo')"),
            Event(EventType.EXECUTE_CELL, 0),
            Event(EventType.SAVE_NOTEBOOK, None),
            Event(EventType.REMOVE_CELL, 0),
        ]
        for event in events:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            self.event_queue.append(event)
            logger.info("Evento producido: %s", event.event_type)

    async def event_consumer(self):
        while True:
            if self.event_queue:
                event = self.event_queue.popleft()
                handler = self.event_handlers.get(event.event_type)
                if handler:
                    try:
                        await handler(event.data)
                    except Exception as e:
                        logger.error("Error al manejar evento %s: %s", event.event_type, e)
            await asyncio.sleep(0.1)

    async def run(self):
        producer_task = asyncio.create_task(self.event_producer())
        consumer_task = asyncio.create_task(self.event_consumer())
        await asyncio.gather(producer_task, consumer_task)

# Ejecutar el bucle de eventos
async def main():
    event_loop = EventLoop()
    await event_loop.run()

if __name__ == "__main__":
    asyncio.run(main())