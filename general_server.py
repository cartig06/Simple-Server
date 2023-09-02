import socket, threading, keyboard as kb, time

#i am fully aware of the errors upon closing the server with CTRL+C. I am still figuring this out, however
#i believe it has something to do with closing the threads for the sockets. Any advice would be appreciated
#because i am still a novice at best when it comes to python

class Server():
    def __init__(self, port):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.addr = (self.host, port)
        self.format = 'utf-8'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen()
        self.running = True
        self.conns = []
    
    def run(self):
        print("[SERVER] Server started!")
        kb.add_hotkey('ctrl+c', self.stop)
        while self.running:
            conn, addr = self.sock.accept()
            client_thread = threading.Thread(target=self.handle, args=(conn, addr))
            client_thread.start()

    def handle(self, conn, addr):
        self.conns.append(conn)
        listening = True
        while listening:
            buffer_size = conn.recv(1024)
            try:
                buffer_size = int(buffer_size.decode(self.format))
                client_message = conn.recv(buffer_size).decode(self.format)
            except:
                client_message = "Error Recieving Buffer Size! Value Not of Type: Integer"
            if client_message == "!QUIT":
                conn.close()
                print(f"[TERMINATED] Killing Connection to {addr[0]}")
                listening = False
            elif client_message == "!ACTIVE":
                active = str(threading.active_count())
                conn.send(str(len(active)).encode(self.format))
                conn.send(active.encode(self.format))
                print(f"[SERVER] Sent Active User Count({active}) to User {addr[0]}")
            else:
                print(f"[{addr[0]}] {client_message}")

    def stop(self):
        print('\nStopping Server...')
        self.running = False
        time.sleep(1)
        if len(self.conns) > 0:
            for conn in self.conns:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                except Exception as e:
                    print(f"Error closing socket: couldnt close socket...\n{e}")
        self.sock.close()

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message):
        self.sock.send(str(len(message)).encode('utf-8'))
        self.sock.send(message.encode('utf-8'))

    def connect(self):
        self.sock.connect(self.addr)
        print("[SERVER] Connected!")
        connected = True
        while connected:
            message = input("Send> ")
            if message == "!ACTIVE":
                self.send(message=message)
                active_len = self.sock.recv(1024)
                try:
                    active_len = int(active_len)
                    active_users = self.sock.recv(active_len)
                    print(f"There are {active_users} users active!")
                except:
                    print("Invalid Length!")
            elif message == "!QUIT":
                self.send(message=message)
                connected = False
                self.sock.close()
            else:
                self.send(message=message)


    
if __name__ == "__main__":
    print("Please do not run the server from source script! Starting Server on 4444...")
    print("Note: This is a test server. For further implementation, please use 'import general_server'")
    print("For basic usage, a simple 'server = general_server.Server(*port*) should do.'")
    print("feel free to create your own uses and fork this project to your heart's content")
    print("p.s. Don't forget to run the server once declared! (server.run())")
    serv = Server(4444)
    serv.run()
