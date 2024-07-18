import asyncio
import random

# Simulación de microservicios con retardos y fallos aleatorios
async def microservice_1():
    """
    Simula un microservicio con un retardo de 1 segundo y una probabilidad
    de fallo del 20%.
    """
    await asyncio.sleep(1)  # Retardo de 1 segundo
    if random.random() < 0.2:  # 20% de probabilidad de fallo
        raise Exception("Microservice 1 failed")
    return "Microservice 1 response"

async def microservice_2():
    """
    Simula un microservicio con un retardo de 2 segundos y una probabilidad
    de fallo del 20%.
    """
    await asyncio.sleep(2)  # Retardo de 2 segundos
    if random.random() < 0.2:  # 20% de probabilidad de fallo 
        raise Exception("Microservice 2 failed")
    return "Microservice 2 response"

async def microservice_3():
    """
    Simula un microservicio con un retardo de 3 segundos y una probabilidad
    de fallo del 20%.
    """
    await asyncio.sleep(3)  # Retardo de 3 segundos 
    if random.random() < 0.2:  # 20% de probabilidad de fallo
        raise Exception("Microservice 3 failed")
    return "Microservice 3 response"

# Coordinador que gestiona la comunicación entre los microservicios
async def coordinator():
    """
    Gestiona la comunicación entre varios microservicios y maneja las respuestas.
    También maneja los posibles fallos de comunicación.
    """
    tasks = [
        microservice_1(),
        microservice_2(),
        microservice_3()
    ]
    
    responses = []
    
    # Maneja las respuestas y posibles excepciones de los microservicios
    for task in asyncio.as_completed(tasks):
        try:
            response = await task
            responses.append(response)
        except Exception as e:
            responses.append(str(e))
    
    return responses

# Función principal para ejecutar el coordinador y mostrar las respuestas
async def main():
    """
    Ejecuta el coordinador y muestra las respuestas de los microservicios.
    """
    responses = await coordinator()
    for response in responses:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())