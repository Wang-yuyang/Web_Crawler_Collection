#! python3


import socket
import sys

def scan():
    ip = "175.24.98.38"
    for port in range(20,100):
        try:
            s = socket.socket()
            print ("[+] Attempting to conect to %s : %d"%(ip,port))
            s.connect((ip,port))
            # s.send('scan')
            banner = s.recv(1024)
            
            if banner:
                print ("[+] PORT-%d- :: %s"%(port , str(banner)))
            s.connect()
        except:
            pass

def main():
    scan()

if __name__ == "__main__":
    main()
