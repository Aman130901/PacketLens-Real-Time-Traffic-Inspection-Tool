from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.dns import DNS, DNSQR


class PacketDecoder:

    @staticmethod
    def decode(packet):

        info = {
            "src_mac": "-",
            "dst_mac": "-",
            "src_ip": "-",
            "dst_ip": "-",
            "protocol": "-",
            "src_port": "-",
            "dst_port": "-",
            "length": len(packet),
            "dns_query": "-",
            "tcp_flags": "-",
            "ttl": "-"
        }

        # Ethernet
        if Ether in packet:
            eth = packet[Ether]
            info["src_mac"] = eth.src
            info["dst_mac"] = eth.dst

        # ARP
        if ARP in packet:
            arp = packet[ARP]
            info["protocol"] = "ARP"
            info["src_ip"] = arp.psrc
            info["dst_ip"] = arp.pdst
            return info

        # IPv4
        if IP in packet:

            ip = packet[IP]

            info["src_ip"] = ip.src
            info["dst_ip"] = ip.dst
            info["ttl"] = ip.ttl

        # TCP
        if TCP in packet:

            tcp = packet[TCP]

            info["protocol"] = "TCP"
            info["src_port"] = tcp.sport
            info["dst_port"] = tcp.dport
            info["tcp_flags"] = str(tcp.flags)

        # UDP
        elif UDP in packet:

            udp = packet[UDP]

            info["protocol"] = "UDP"
            info["src_port"] = udp.sport
            info["dst_port"] = udp.dport

        # ICMP
        elif ICMP in packet:

            info["protocol"] = "ICMP"

        # DNS
        if DNS in packet:

            dns = packet[DNS]

            if dns.qr == 0 and DNSQR in packet:

                info["dns_query"] = dns[DNSQR].qname.decode(errors="ignore")

        return info