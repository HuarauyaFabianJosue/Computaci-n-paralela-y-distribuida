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