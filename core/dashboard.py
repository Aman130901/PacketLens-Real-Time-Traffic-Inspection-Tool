from rich.table import Table


class Dashboard:

    @staticmethod
    def build(stats):

        # Dashboard Table
        dashboard = Table(title="📡 PacketLens Live Dashboard")

        dashboard.add_column("Metric", style="cyan")
        dashboard.add_column("Value", style="green")

        dashboard.add_row("Total Packets", str(stats.total))
        dashboard.add_row("TCP", str(stats.tcp))
        dashboard.add_row("UDP", str(stats.udp))
        dashboard.add_row("ICMP", str(stats.icmp))
        dashboard.add_row("ARP", str(stats.arp))
        dashboard.add_row("Other", str(stats.other))

        dashboard.add_row("Last Source", stats.last_src)
        dashboard.add_row("Last Destination", stats.last_dst)
        dashboard.add_row("Last Protocol", stats.last_protocol)

        # History Table
        history = Table(title="Recent Packets")

        history.add_column("Protocol")
        history.add_column("Source")
        history.add_column("Destination")
        history.add_column("Port")
        history.add_column("DNS")

        for packet in reversed(stats.history):

            history.add_row(
                packet["protocol"],
                str(packet["src_ip"]),
                str(packet["dst_ip"]),
                str(packet["dst_port"]),
                str(packet.get("dns_query", "-"))
            )

        return dashboard, history