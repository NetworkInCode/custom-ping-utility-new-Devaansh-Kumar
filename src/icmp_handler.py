import struct
import time
import select
from checksum import calculate_checksum

ICMP_ECHO_REQUEST = 8
ICMPV6_ECHO_REQUEST = 128

payload = b'\x50\x49\x4E\x47\x2D\x50\x4F\x4E\x47\x20\x46\x52\x4F\x4D' \
          b'\x20\x5A\x4D\x45\x59\x32\x30\x30\x30\x30\x40\x59\x41\x48' \
          b'\x4F\x4F\x2E\x43\x4F\x4D'

def create_icmp_packet(seq, use_ipv6, packet_id):
    """Create ICMP echo request packet."""

    if use_ipv6:
        header = struct.pack("!BbHHh", ICMPV6_ECHO_REQUEST, 0, 0, packet_id, seq)
        checksum = calculate_checksum(header + payload)
        header = struct.pack("!BbHHh", ICMPV6_ECHO_REQUEST, 0, checksum, packet_id, seq)
        return header + payload
    else:
        header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, packet_id, seq)
        checksum = calculate_checksum(header + payload)
        header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum, packet_id, seq)
        return header + payload

def receive_ping(sock, sent_time, timeout, use_ipv6, packet_id):
    """Receive and validate the ping reply."""
    time_left = timeout

    while True:
        start_time = time.time()
        ready = select.select([sock], [], [], time_left)
        time_spent = time.time() - start_time

        if ready[0] == []:  # Timeout
            return None, None

        time_received = time.time()
        recv_packet, addr = sock.recvfrom(1024)

        if use_ipv6:
            icmp_header = recv_packet[0:8]
            packet_type, code, checksum, recv_packet_id, sequence = struct.unpack("!BbHHh", icmp_header)
        else:
            icmp_header = recv_packet[20:28]
            packet_type, code, checksum, recv_packet_id, sequence = struct.unpack("!BBHHH", icmp_header)

        if recv_packet_id == packet_id:  # Packet matches
            return time_received - sent_time, addr

        time_left = time_left - time_spent
        if time_left <= 0:
            return None, None
