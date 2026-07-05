import csv
import json
import os
from scapy.utils import wrpcap


class PacketExporter:

    def __init__(self):

        os.makedirs("exports", exist_ok=True)

        self.csv_file = "exports/packets.csv"
        self.json_file = "exports/packets.json"
        self.pcap_file = "exports/capture.pcap"

        self.raw_packets = []

        if not os.path.exists(self.csv_file):

            with open(self.csv_file, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Source IP",
                    "Destination IP",
                    "Protocol",
                    "Source Port",
                    "Destination Port",
                    "Length"
                ])

    def export(self, info, raw_packet):

        # ---------- CSV ----------

        with open(self.csv_file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                info["src_ip"],
                info["dst_ip"],
                info["protocol"],
                info["src_port"],
                info["dst_port"],
                info["length"]
            ])

        # ---------- JSON ----------

        data = []

        if os.path.exists(self.json_file):

            try:
                with open(self.json_file) as f:
                    data = json.load(f)

            except:
                data = []

        data.append(info)

        with open(self.json_file, "w") as f:

            json.dump(data, f, indent=4)

        # ---------- PCAP ----------

        self.raw_packets.append(raw_packet)

        wrpcap(self.pcap_file, self.raw_packets)