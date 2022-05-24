#!/bin/python3

from math import ceil
import multiprocessing
import os

import sys
import socket
from datetime import datetime

proc_list = []
end_range = []
open_ports = []

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)  # test, timeout in 1sec
    result = sock.connect_ex((target, port))  # return error indicator
    if result == 0:
        print("Open port found: " + str(port))
        open_ports.append(port)
    sock.close()  # close connection.

def make_range_list(r_start, r_end):
    end_range.append(r_start)
    step = ceil((r_end - r_start) / os.cpu_count()) #(85-50)/8

    x = r_start
    while x in range(r_start, r_end):
        x += step
        end_range.append(x)

def scan_ranges(ip):
        try:
            for port in range(end_range.pop(0), end_range[0]):
                #print(multiprocessing.current_process().pid)
                print("\nScanning port: " + str(port))
                scan_port(ip, port)
        except IndexError:
            pass

def main():
    ip_address = 0

    if len(sys.argv) >= 4:
        ip_address = socket.gethostbyname(sys.argv[1])
    else:
        print("Syntax Error: \n python PortScanner [192.168.53.1] [StartPort] [EndPort]")

    r_start = sys.argv[2]
    r_end = sys.argv[3]
    make_range_list(int(r_start), int(r_end))

    print("-" * 55)
    print("Scanning target..." + ip_address)
    print("Time started: " + str(datetime.now()))
    print("-" * 55)

    try:
        for core in range(os.cpu_count()):
            p = multiprocessing.Process(target=scan_ranges(ip_address))
            p.start()
            proc_list.append(p)

    except KeyboardInterrupt:
        print("Scan interrupted.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Unable to connect.")
        sys.exit()

    for p in proc_list:
        p.join()
    print("-" * 55)
    print("Scan finished: " + str(datetime.now()))
    if len(open_ports) > 0:
        for port in open_ports:
            print("Port %d open." %port)
    else:
        print("No open ports found.")
    print("-" * 55)

if __name__ == '__main__':
    main()