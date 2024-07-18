### Pregunta 4 (5 puntos): Sistema de monitoreo de recursos del sistema

Para desarrollar un sistema de monitoreo de recursos del sistema utilizando `asyncio` y `concurrent.futures`, seguiremos los requisitos:

1. **Utilizar `asyncio` para ejecutar comandos del sistema de manera asíncrona.**
2. **Utilizar `concurrent.futures.ThreadPoolExecutor` o `concurrent.futures.ProcessPoolExecutor` para procesar los resultados en paralelo.**
3. **Implementar una interfaz de línea de comandos para especificar qué recursos monitorear y con qué frecuencia.**
4. **Guardar los resultados en un archivo de log.**
5. **Implementar un sistema de notificación para alertar al usuario si los recursos exceden ciertos umbrales.**

### Implementación

#### `monitor.py`
```python
import asyncio
import concurrent.futures
import logging
import os
import time
from datetime import datetime
import psutil

# Configuración de logging
logging.basicConfig(filename='resource_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Función para obtener el uso de la CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Función para obtener el uso de la memoria
def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return memory_info.percent

# Función para obtener el uso del disco
def get_disk_usage():
    disk_info = psutil.disk_usage('/')
    return disk_info.percent

# Función para manejar el monitoreo de recursos
async def monitor_resource(executor, resource_func, resource_name, threshold):
    loop = asyncio.get_event_loop()
    while True:
        usage = await loop.run_in_executor(executor, resource_func)
        logging.info(f'{resource_name} usage: {usage}%')
        if usage > threshold:
            logging.warning(f'{resource_name} usage exceeded threshold: {usage}%')
            print(f'ALERT: {resource_name} usage exceeded threshold: {usage}%')
        await asyncio.sleep(1)

# Función principal para configurar el monitoreo
async def main(resources_to_monitor, frequency, thresholds):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(resources_to_monitor))
    tasks = []
    for resource, threshold in zip(resources_to_monitor, thresholds):
        if resource == 'cpu':
            tasks.append(monitor_resource(executor, get_cpu_usage, 'CPU', threshold))
        elif resource == 'memory':
            tasks.append(monitor_resource(executor, get_memory_usage, 'Memory', threshold))
        elif resource == 'disk':
            tasks.append(monitor_resource(executor, get_disk_usage, 'Disk', threshold))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Sistema de monitoreo de recursos del sistema.')
    parser.add_argument('--resources', nargs='+', choices=['cpu', 'memory', 'disk'], required=True, help='Recursos a monitorear.')
    parser.add_argument('--frequency', type=int, default=5, help='Frecuencia de monitoreo en segundos.')
    parser.add_argument('--thresholds', nargs='+', type=int, required=True, help='Umbrales para alertas.')

    args = parser.parse_args()

    if len(args.resources) != len(args.thresholds):
        print('El número de recursos debe coincidir con el número de umbrales.')
        exit(1)

    asyncio.run(main(args.resources, args.frequency, args.thresholds))
```

### Explicación del Código

1. **Configuración de Logging:**
   - Se configura el logging para guardar los resultados del monitoreo en un archivo de log llamado `resource_monitor.log`.

2. **Funciones de Monitoreo:**
   - `get_cpu_usage`: Obtiene el uso de la CPU.
   - `get_memory_usage`: Obtiene el uso de la memoria.
   - `get_disk_usage`: Obtiene el uso del disco.

3. **Función `monitor_resource`:**
   - Ejecuta la función de monitoreo de recursos en un `ThreadPoolExecutor` y registra los resultados. Si el uso del recurso excede el umbral especificado, se genera una alerta.

4. **Función `main`:**
   - Configura el `ThreadPoolExecutor` y crea las tareas de monitoreo para los recursos especificados.

5. **Interfaz de Línea de Comandos:**
   - Se utiliza `argparse` para permitir que el usuario especifique los recursos a monitorear, la frecuencia de monitoreo y los umbrales para las alertas desde la línea de comandos.

### Instrucciones para la ejecución:

1. **Ejecutar el script con los argumentos apropiados:**
   ```bash
   python Pregunta4.py --resources cpu memory disk --frequency 5 --thresholds 75 80 85
   ```

### Resultado 

![alt text](<Captura desde 2024-07-18 09-37-36.png>)