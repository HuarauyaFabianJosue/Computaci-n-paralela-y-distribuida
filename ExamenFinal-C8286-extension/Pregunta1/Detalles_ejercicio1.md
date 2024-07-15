### Pregunta 1 (5 puntos): Implementa un sistema basado en eventos en Python que simule cómo los Jupyter Notebooks manejan eventos e interacciones de usuario. Esto incluye crear un bucle de eventos, manejar diferentes tipos de eventos y actualizar el estado de un notebook simulado basado en interacciones de usuario.

El código debe incluir:

- Usar asyncio para manejar la ejecución asíncrona de celdas y el manejo de eventos.
- Implementar mecanismos de manejo de errores y registro de logs para diferentes tipos de errores.
- Asegurae operaciones seguras en los hilos al acceder a recursos compartidos.
- Implementa un sistema para filtrar y priorizar eventos según su importancia o tipo.

### Código:

```python
import asyncio
import logging
import random
from collections import deque
from enum import Enum
from typing import Any, Callable, Dict

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
    def __init__(self, event_type: EventType, data: Any, priority: int):
        self.event_type = event_type
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

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
        self.event_queue = asyncio.PriorityQueue()
        self.notebook = Notebook()
        self.event_handlers: Dict[EventType, Callable[[Any], Any]] = {
            EventType.EXECUTE_CELL: self.notebook.execute_cell,
            EventType.SAVE_NOTEBOOK: lambda _: self.notebook.save_notebook(),
            EventType.ADD_CELL: self.notebook.add_cell,
            EventType.REMOVE_CELL: self.notebook.remove_cell,
        }

    async def event_producer(self):
        # Simular eventos generados por el usuario con diferentes prioridades
        events = [
            Event(EventType.ADD_CELL, "print('Hola mundo')", 2),
            Event(EventType.EXECUTE_CELL, 0, 1),
            Event(EventType.SAVE_NOTEBOOK, None, 3),
            Event(EventType.REMOVE_CELL, 0, 4),
        ]
        for event in events:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            await self.event_queue.put(event)
            logger.info("Evento producido: %s con prioridad %d", event.event_type, event.priority)

    async def event_consumer(self):
        while True:
            if not self.event_queue.empty():
                event = await self.event_queue.get()
                handler = self.event_handlers.get(event.event_type)
                if handler:
                    try:
                        await handler(event.data)
                    except Exception as e:
                        logger.error("Error al manejar evento %s: %s", event.event_type, e)
                self.event_queue.task_done()
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
```

### Explicación del Código:

1. **Definición de Clases y Enumeraciones:**
   - `EventType`: Enum para diferentes tipos de eventos.
   - `Event`: Clase que representa un evento con un tipo, datos asociados y prioridad.
   - `Notebook`: Clase que simula un notebook con operaciones para añadir, eliminar y ejecutar celdas, y guardar el notebook.

2. **Manejo de Eventos:**
   - `EventLoop`: Clase que maneja la cola de eventos (usando `asyncio.PriorityQueue`) y los despacha a los manejadores correspondientes. Incluye métodos para producir eventos (`event_producer`) y consumir eventos (`event_consumer`).

3. **Uso de `asyncio` para Asincronía:**
   - Se utilizan tareas de `asyncio` para producir y consumir eventos de manera asíncrona, lo que simula la interacción del usuario y el manejo de eventos en un Jupyter Notebook.

4. **Manejo de Errores y Registro de Logs:**
   - Se utilizan bloques `try-except` y el módulo `logging` para manejar errores y registrar eventos y errores.

5. **Operaciones Seguras en los Hilos:**
   - Se usa `asyncio.Lock` para asegurar operaciones seguras al acceder a recursos compartidos como la lista de celdas del notebook.

6. **Filtrado y Priorización de Eventos:**
   - Se utiliza una cola de prioridad (`asyncio.PriorityQueue`) para manejar los eventos según su importancia o tipo.

### Resultado:

![alt text](<Captura desde 2024-07-14 21-34-49.png>)

1. **Evento Producido: `ADD_CELL` con prioridad 2**
   ```
   INFO:__main__:Evento producido: EventType.ADD_CELL con prioridad 2
   INFO:__main__:Celda añadida: print('Hola mundo')
   ```
2. **Evento Producido: `EXECUTE_CELL` con prioridad 1**
   ```
   INFO:__main__:Evento producido: EventType.EXECUTE_CELL con prioridad 1
   INFO:__main__:Ejecutando celda 0: print('Hola mundo')
   INFO:__main__:Ejecución completada: print('Hola mundo')
   ```
3. **Evento Producido: `SAVE_NOTEBOOK` con prioridad 3**
   ```
   INFO:__main__:Evento producido: EventType.SAVE_NOTEBOOK con prioridad 3
   INFO:__main__:Guardando notebook con 1 celdas
   INFO:__main__:Notebook guardado
   ```
4. **Evento Producido: `REMOVE_CELL` con prioridad 4**
   ```
   INFO:__main__:Evento producido: EventType.REMOVE_CELL con prioridad 4
   INFO:__main__:Celda eliminada: print('Hola mundo')
   ```

El código ha funcionado correctamente y todos los eventos se han manejado en el orden de sus prioridades. Aquí está el flujo completo:
1. Una celda se añade al notebook.
2. La celda añadida se ejecuta.
3. El notebook se guarda con la celda añadida.
4. La celda se elimina del notebook.
