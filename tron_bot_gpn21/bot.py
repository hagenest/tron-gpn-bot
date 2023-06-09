import socket
import random

url = "http://gpn-tron.duckdns.org"
default_ip = "94.45.236.142"
port = 4000
default_name = "hagi-tron"
version = "0.1"
password = "oieshgfgh432trewoigfh4w98hoihjkj2"
moves = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

class Bot:
    def __init__(self, name=default_name, version=version):
        self.name = name
        self.version = version
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((default_ip, port))
        self.socket.sendall(bytes(f"join|{self.name}-{self.version}|{password}\n", "utf-8"))
        # self.socket.sendall(bytes(self.version + "\n", "utf-8"))
        # self.socket.sendall(bytes("join\n", "utf-8"))
        self.socket.settimeout(0.5)
        self.used_pos = []
        self.current_pos = (0, 0)
        self.id = 0

    def listen(self):
        try:
            return self.socket.recv(1024).decode("utf-8")
        except socket.timeout:
            return "Timeout"
        except socket.error:
            return "Error"

    def play(self):
        for res in self.read_line():
            if res[0] == "game":
                self.id = int(res[3])
                self.used_pos = []
            if res[0] == "pos":
                if int(res[1]) == self.id:
                    self.current_pos = (int(res[2]), int(res[3]))
                self.used_pos.append((int(res[2]), int(res[3])))
                print("current_pos:", self.current_pos)
                print("used:", self.used_pos)
            if res[0] == "tick":
                dir = ""
                for i in range(100): # I don't like this
                    dir = random.choice(list(moves.keys()))
                    print("Try dir", dir)
                    future_pos = (self.current_pos[0] + moves[dir][0], self.current_pos[1] + moves[dir][1])
                    if future_pos not in self.used_pos:
                        break
                self.socket.sendall(bytes(f"move|{dir}\n", "utf-8"))
                print("Move", dir)
            if res[0] == "lose":
                print("lose")
        
        
    def read_line(self):
        while True:
            res = self.listen()
            print(res)
            for line in res.splitlines():
                yield line.split("|")

if __name__ == "__main__":
    bot = Bot()
    print("init bot")
    bot.play()