### Pregunta 2 (5 puntos): Desarrolla un simulador de red P2P (peer-to-peer) donde varios nodos pueden enviar y recibir mensajes de manera asíncrona.

Para desarrollar un simulador de red P2P (peer-to-peer) sequiremos los requisitos:

1. **Utilizar `asyncio` para gestionar la comunicación entre los nodos de la red.**
2. **Cada nodo debe poder enviar y recibir mensajes a/de otros nodos.**
3. **Implementar una interfaz de línea de comandos para que el usuario pueda agregar, eliminar nodos y enviar mensajes.**
4. **Implementar un mecanismo para manejar la concurrencia en el envío y recepción de mensajes.**
5. **Asegurar que la red sea robusta y maneje errores de comunicación adecuadamente.**

### Implementación


```python
import asyncio
import random

class Node:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.inbox = asyncio.Queue()
        self.peers = []

    async def send_message(self, message, recipient_id):
        await asyncio.sleep(random.uniform(0.1, 1))  # Simula latencia de red
        if recipient_id in self.network.nodes:
            await self.network.nodes[recipient_id].inbox.put((self.node_id, message))
        else:
            print(f"Node {recipient_id} not found in the network.")

    async def receive_messages(self):
        while True:
            sender_id, message = await self.inbox.get()
            print(f"Node {self.node_id} received message from Node {sender_id}: {message}")

class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        if node_id not in self.nodes:
            new_node = Node(node_id, self)
            self.nodes[node_id] = new_node
            asyncio.create_task(new_node.receive_messages())
            print(f"Node {node_id} added to the network.")
        else:
            print(f"Node {node_id} already exists.")

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"Node {node_id} removed from the network.")
        else:
            print(f"Node {node_id} not found in the network.")

    async def send_message(self, sender_id, recipient_id, message):
        if sender_id in self.nodes:
            await self.nodes[sender_id].send_message(message, recipient_id)
        else:
            print(f"Sender Node {sender_id} not found in the network.")

async def main():
    network = Network()

    while True:
        print("\nOptions:")
        print("1. Add Node")
        print("2. Remove Node")
        print("3. Send Message") 
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            node_id = input("Enter Node ID to add: ")
            network.add_node(node_id)
        elif choice == "2":
            node_id = input("Enter Node ID to remove: ")
            network.remove_node(node_id)
        elif choice == "3":
            sender_id = input("Enter Sender Node ID: ")
            recipient_id = input("Enter Recipient Node ID: ")
            message = input("Enter Message: ")
            await network.send_message(sender_id, recipient_id, message)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Explicación del Código:

1. **Clase `Node`:**
   - **`__init__`**: Inicializa el nodo con un ID, referencia a la red y una cola de mensajes (`inbox`).
   - **`send_message`**: Envía un mensaje a otro nodo con un retardo aleatorio para simular la latencia de red.
   - **`receive_messages`**: Recibe mensajes de otros nodos y los imprime. 

2. **Clase `Network`:**
   - **`__init__`**: Inicializa una red vacía de nodos.
   - **`add_node`**: Agrega un nuevo nodo a la red.
   - **`remove_node`**: Elimina un nodo de la red.
   - **`send_message`**: Envia un mensaje desde un nodo a otro en la red.

3. **Función `main`:**
   - Implementa una interfaz de línea de comandos para que el usuario pueda agregar, eliminar nodos y enviar mensajes.

### Cumplimiento de los Requisitos:

1. **Utiliza `asyncio` para gestionar la comunicación entre los nodos de la red.**
   - Sí, se usa `asyncio` para gestionar la comunicación asíncrona entre los nodos.
   
2. **Cada nodo debe poder enviar y recibir mensajes a/de otros nodos.**
   - Sí, cada nodo puede enviar y recibir mensajes mediante las funciones `send_message` y `receive_messages`.

3. **Implementar una interfaz de línea de comandos para que el usuario pueda agregar, eliminar nodos y enviar mensajes.**
   - Sí, la función `main` proporciona una interfaz de línea de comandos para interactuar con la red.

4. **Implementar un mecanismo para manejar la concurrencia en el envío y recepción de mensajes.**
   - Sí, se utiliza `asyncio.Queue` para manejar la concurrencia en la recepción de mensajes.

5. **Asegura que la red sea robusta y maneje errores de comunicación adecuadamente.**
   - Se manejan errores como nodos inexistentes y se imprime un mensaje de error en esos casos.

### Resultado

![alt text](<Captura desde 2024-07-18 09-26-37.png>)