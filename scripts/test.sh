#!/bin/bash

# Run as: sudo bash test.sh
# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo!"
  exit 1
fi

# Define the path to the custom ping script
PING_SCRIPT="../src/main.py"

echo "=== Starting Test Suite for Custom Ping Utility ==="

# 1. Basic IPv4 ping with default options
echo -e "\n[TEST 1] Basic IPv4 ping with 4 packets and TTL 64"
echo "Command: sudo python3 $PING_SCRIPT google.com"
sudo python3 $PING_SCRIPT google.com

# 2. Basic IPv6 ping with 4 packets and TTL 64
echo -e "\n[TEST 2] Basic IPv6 ping with 4 packets and TTL 64"
echo "Command: sudo python3 $PING_SCRIPT google.com -6"
sudo python3 $PING_SCRIPT google.com -6

# 3. Ping with 5 packets and TTL 128
echo -e "\n[TEST 3] Ping with 5 packets and TTL 128"
echo "Command: sudo python3 $PING_SCRIPT google.com -c 5 -t 128"
sudo python3 $PING_SCRIPT google.com -c 5 -t 128

# 4. Ping using a specific network interface (eth0 or change if needed)
INTERFACE="enp1s0f0"
echo -e "\n[TEST 4] Ping with 3 packets and using interface $INTERFACE"
echo "Command: sudo python3 $PING_SCRIPT google.com -c 3 -i $INTERFACE"
sudo python3 $PING_SCRIPT google.com -c 3 -i $INTERFACE

# 5. IPv6 ping with custom timeout and 6 packets
echo -e "\n[TEST 5] IPv6 ping with 6 packets and 2 seconds timeout"
echo "Command: sudo python3 $PING_SCRIPT google.com -c 6 --timeout 2 -6"
sudo python3 $PING_SCRIPT google.com -c 6 --timeout 2 -6

# 6. Ping an IPv4 address explicitly
echo -e "\n[TEST 6] Ping IPv4 address 1.1.1.1 with 4 packets"
echo "Command: sudo python3 $PING_SCRIPT 1.1.1.1"
sudo python3 $PING_SCRIPT 1.1.1.1

# 7. Ping an IPv6 address explicitly
echo -e "\n[TEST 7] Ping IPv6 address 2606:4700:4700::1111 with 4 packets"
echo "Command: sudo python3 $PING_SCRIPT 2606:4700:4700::1111 -6"
sudo python3 $PING_SCRIPT 2606:4700:4700::1111 -6

# 8. Ping with large packet count and interrupt to check statistics
echo -e "\n[TEST 8] Ping with 10 packets and interrupt with Ctrl+C"
echo "Command: sudo python3 $PING_SCRIPT google.com -c 10"
echo "Manually interrupt after 3-4 packets to check statistics."
sudo python3 $PING_SCRIPT google.com -c 10

# 9. Ping with minimum TTL (1) to observe TTL exceeded
echo -e "\n[TEST 9] Ping with TTL=1 to induce TTL exceeded error"
echo "Command: sudo python3 $PING_SCRIPT google.com -t 1"
sudo python3 $PING_SCRIPT google.com -t 1

# 10. Invalid domain to test error handling
echo -e "\n[TEST 10] Invalid domain to test error handling"
echo "Command: sudo python3 $PING_SCRIPT invalid-domain.com"
sudo python3 $PING_SCRIPT invalid-domain.com

echo -e "\n=== Test Suite Completed! ==="
