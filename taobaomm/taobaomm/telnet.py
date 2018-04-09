import sys
import getpass
import telnetlib

HOST = "localhost"

def main():
    ports = ['6023']
    if len(sys.argv) > 1:
        ports = sys.argv[1].split(',')

    for port in ports:
        get_stats(port)

def get_stats(port):
    tn = telnetlib.Telnet(HOST, port)
    tn.read_until(b'>>>')
    tn.write(b"engine.unpause()\n")

    print(tn.read_until(b'>>>'))
    tn.close()

if __name__ == '__main__':
    main()