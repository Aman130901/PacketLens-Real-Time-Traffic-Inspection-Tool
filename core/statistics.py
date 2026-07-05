from collections import deque


class PacketStatistics:

    def __init__(self):

        self.total = 0
        self.tcp = 0
        self.udp = 0
        self.icmp = 0
        self.arp = 0
        self.other = 0

        self.last_src = "-"
        self.last_dst = "-"
        self.last_protocol = "-"

        # Store last 10 packets
        self.history = deque(maxlen=10)

    def update(self, packet):

        self.total += 1

        protocol = packet["protocol"]

        if protocol == "TCP":
            self.tcp += 1

        elif protocol == "UDP":
            self.udp += 1

        elif protocol == "ICMP":
            self.icmp += 1

        elif protocol == "ARP":
            self.arp += 1

        else:
            self.other += 1

        self.last_src = packet["src_ip"]
        self.last_dst = packet["dst_ip"]
        self.last_protocol = protocol

        self.history.append(packet)