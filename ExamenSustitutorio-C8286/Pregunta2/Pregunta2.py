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