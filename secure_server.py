import socket
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 5555

class ChatServer:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        print(f"[*] Server listening on {host}:{port}")
        print("[*] Waiting for connections...")

    def broadcast(self, message, sender_socket=None):
        """
        Sends a message to all connected clients except the sender.
        """
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # Remove broken connections
                    self.remove(client)

    def handle_client(self, client):
        """
        Handles incoming messages from a specific client.
        """
        while True:
            try:
                # Receive message
                message = client.recv(4096)
                if not message:
                    break
                
                # Broadcast the raw encrypted bytes to others
                self.broadcast(message, sender_socket=client)
            except:
                break
        
        self.remove(client)

    def remove(self, client):
        """
        Removes a client from the list and closes the connection.
        """
        if client in self.clients:
            self.clients.remove(client)
            client.close()

    def run(self):
        """
        Main loop to accept new connections.
        """
        while True:
            client, address = self.server.accept()
            print(f"[+] Connected with {str(address)}")
            
            self.clients.append(client)
            
            # Start a thread to handle this client
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.run()