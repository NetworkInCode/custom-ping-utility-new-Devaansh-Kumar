[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/waUhK5p8)
# Custom Ping Utility
This is a Python based implementation of ping that can send ICMP Echo Requests and receive ICMP Echo Responses and display helpful statistics.
It supports both IPv4 and IPv6 and has a lot of configurable options like ping count, ttl, network interface and timeout.
---

## **Features Implemented**

- **Send ICMP echo requests** to a target IP address.
- **Receive and process ICMP echo replies** from the target.
- **Calculate and display round-trip time (RTT)** for each ICMP echo request-reply cycle.
- **Provides statistics** on:
  - Packet loss
  - Minimum RTT
  - Maximum RTT
  - Average RTT
  - Standard deviation of RTT
- **Provide options** to configure the utility:
  - Choose the network interface for sending packets.
  - Set the Time-To-Live (TTL) value.
  - Support both **IPv4 and IPv6**.
  - Set No. of packets to send
  - Set timeout value
- Handles **keyboard interruptions (`Ctrl + C`)** gracefully to show intermediate statistics.
- Error handling for invalid domain names or unreachable IPs.
- Provides extensive test cases and logging options.

---

## **🚀 Getting Started**

### 1. Clone the repository
```bash
git clone https://github.com/NetworkInCode/custom-ping-utility-new-Devaansh-Kumar custom_ping
cd custom_ping
```

The only dependency is to have Python 3 installed and Linux.

### 2. Run the utility
```bash
sudo python3 src/main.py google.com
```

You can also use Make to run the utility and set options
```bash
COUNT=5 TARGET=amazon.com make run
```
---

## **Usage**
```bash
usage: main.py [-h] [-c COUNT] [-t TTL] [-i INTERFACE] [--timeout TIMEOUT] [-6] destination

Custom Ping Utility

positional arguments:
  destination           Target hostname or IP address

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of packets to send (default: 4)
  -t TTL, --ttl TTL     Time-To-Live (TTL) value for packets (default: 64)
  -i INTERFACE, --interface INTERFACE
                        Network interface to use for sending packets (optional)
  --timeout TIMEOUT     Timeout in seconds for each packet (default: 1)
  -6, --ipv6            Use IPv6 instead of IPv4 (defualt: false)
```
---

## **Examples**
1. Basic IPv4 Ping
```bash
 sudo python3 src/main.py google.com
```
2. Ping with 5 Packets and TTL 128
```bash
 sudo python3 src/main.py google.com -c 5 -t 128
```
3. Use a Specific Network Interface (eth0)
```bash
 sudo python3 src/main.py google.com -c 3 -i eth0
 ```
4. Ping Using IPv6
```bash
 sudo python3 src/main.py google.com -6
 ```
5. Ping an IPv4 Address Explicitly
```bash
 sudo python3 src/main.py 1.1.1.1
 ```
6. Ping an IPv6 Address
```bash
 sudo python3 src/main.py 2606:4700:4700::1111 -6
```
7. Set Timeout Value
```bash
 sudo python3 src/main.py google.com --timeout 2
```
---

## **Run Test Suite**
To run all tests and validate the utility use either one of:

```bash
sudo scripts/test.sh
make test
```

To run tests and log the output to a file:
```bash
make test-log
```

## **Cleanup**
```bash
sudo make clean
```

