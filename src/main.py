import socket
import time
import statistics
import sys
import argparse
import os
import signal
from icmp_handler import create_icmp_packet, receive_ping

ICMPV6_PORT = 58

sent_packets = 0
received_packets = 0
rtt_list = []

def signal_handler(sig, frame):
    """Handle interrupt and print statistics."""
    print("\n\nInterrupted! Printing statistics...")
    print_statistics()
    sys.exit(0)

def print_statistics():
    """Print ping statistics and RTT analysis."""
    global sent_packets, received_packets, rtt_list

    packet_loss = (sent_packets - received_packets) / sent_packets * 100 if sent_packets else 0

    if rtt_list:
        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = sum(rtt_list) / len(rtt_list)
        stddev_rtt = statistics.stdev(rtt_list) if len(rtt_list) > 1 else 0
    else:
        min_rtt = max_rtt = avg_rtt = stddev_rtt = 0

    print("\n--- Ping statistics ---")
    print(f"Packets: Sent = {sent_packets}, Received = {received_packets}, Lost = {sent_packets - received_packets} ({packet_loss:.2f}% loss)")
    print(f"RTT (ms): Min = {min_rtt:.2f}, Max = {max_rtt:.2f}, Avg = {avg_rtt:.2f}, Stddev = {stddev_rtt:.2f}")


def ping(destination, count, timeout, interface, ttl, use_ipv6):
    """Perform the ping with all the configured options."""
    global sent_packets, received_packets, rtt_list

    # Get destination IP from hostname
    try:
        family = socket.AF_INET6 if use_ipv6 else socket.AF_INET
        dest_ip = socket.getaddrinfo(destination, None, family=family)[0][4][0]
    except socket.gaierror:
        print(f"Error: Unable to resolve {destination}")
        sys.exit(1)

    print(f"Pinging {destination} [{dest_ip}] with {count} packets using interface {interface} and TTL={ttl} with {'ICMPv6' if use_ipv6 else 'ICMP'}")

    # Create raw socket based on IP version
    address_family = socket.AF_INET6 if use_ipv6 else socket.AF_INET
    proto = socket.IPPROTO_ICMPV6 if use_ipv6 else socket.IPPROTO_ICMP
    sock = socket.socket(address_family, socket.SOCK_RAW, proto)

    # Set interface
    if interface and not use_ipv6:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())
        except Exception as e:
            print(f"Error binding to interface {interface}: {e}")

    # Set Time-To-Live
    if use_ipv6:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
    else:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    # Set timeout value
    sock.settimeout(timeout)

    for seq in range(1, count + 1):
        # Create packet
        packet_id = os.getpid() & 0xFFFF
        packet = create_icmp_packet(seq, use_ipv6, packet_id)
        sent_packets += 1

        # Send Packet
        try:
            if use_ipv6:
                sock.sendto(packet, (dest_ip, ICMPV6_PORT, 0, 0))
            else:
                sock.sendto(packet, (dest_ip, 1))
        except Exception as e:
            print(f"Error in sending packet: {e}")
            break

        sent_time = time.time()
        rtt, addr = receive_ping(sock, sent_time, timeout, use_ipv6, packet_id)

        if rtt is None:
            print(f"Request timed out.")
        else:
            rtt_ms = round(rtt * 1000, 2)
            # print(f"Reply from {addr[0]}: bytes={len(packet)} time={rtt_ms}ms TTL={ttl}")
            print(f"Reply from {addr[0]}: bytes={len(packet)} time={rtt_ms}ms TTL={ttl}")
            received_packets += 1
            rtt_list.append(rtt_ms)

        time.sleep(1)

    sock.close()
    print_statistics()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # Argument parser for CLI options
    parser = argparse.ArgumentParser(description="Custom Ping Utility")

    parser.add_argument("destination", help="Target hostname or IP address")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of packets to send (default: 4)")
    parser.add_argument("-t", "--ttl", type=int, default=64, help="Time-To-Live (TTL) value for packets (default: 64)")
    parser.add_argument("-i", "--interface", help="Network interface to use for sending packets (optional)")
    parser.add_argument("--timeout", type=int, default=1, help="Timeout in seconds for each packet (default: 1)")
    parser.add_argument("-6", "--ipv6", default=False, action="store_true", help="Use IPv6 instead of IPv4 (defualt: false)")

    args = parser.parse_args()

    try:
        ping(args.destination, args.count, args.timeout, args.interface, args.ttl, args.ipv6)
    except PermissionError:
        print("Error: This script requires root/administrator privileges. Run with sudo.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, printing statistics...")
        print_statistics()
        sys.exit(0)
