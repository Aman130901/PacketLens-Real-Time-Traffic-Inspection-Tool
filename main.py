import argparse
import logging

from rich.console import Console

from core.capture import PacketCapture
from core.decoder import PacketDecoder
from core.dashboard import Dashboard
from core.statistics import PacketStatistics
from core.exporter import PacketExporter
from core.report import ReportGenerator

console = Console()

# Configure logging
logging.basicConfig(
    filename="logs/packetlens.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Global objects
stats = PacketStatistics()
exporter = PacketExporter()


def process_packet(packet):
    """
    Callback function executed for every captured packet.
    """

    try:
        # Decode packet
        info = PacketDecoder.decode(packet)

        # Update statistics
        stats.update(info)

        # Export packet
        exporter.export(info, packet)

        # Log packet
        logging.info(
            f"{info['protocol']} | "
            f"{info['src_ip']}:{info['src_port']} -> "
            f"{info['dst_ip']}:{info['dst_port']}"
        )

        # Build dashboard
        dashboard, history = Dashboard.build(stats)

        console.clear()
        console.print("[bold cyan]PacketLens v2.0[/bold cyan]\n")
        console.print(dashboard)
        console.print()
        console.print(history)

    except Exception as e:
        logging.error(str(e))


def main():

    parser = argparse.ArgumentParser(
        description="PacketLens - Real-Time Traffic Inspection Tool"
    )

    parser.add_argument("--interface", help="Network interface")
    parser.add_argument("--tcp", action="store_true")
    parser.add_argument("--udp", action="store_true")
    parser.add_argument("--icmp", action="store_true")
    parser.add_argument("--arp", action="store_true")
    parser.add_argument("--port", type=int)

    args = parser.parse_args()

    # Build capture filter
    bpf_filter = None

    if args.tcp:
        bpf_filter = "tcp"

    elif args.udp:
        bpf_filter = "udp"

    elif args.icmp:
        bpf_filter = "icmp"

    elif args.arp:
        bpf_filter = "arp"

    elif args.port:
        bpf_filter = f"port {args.port}"

    console.print("[bold green]Starting PacketLens...[/bold green]")

    if args.interface:
        console.print(f"[yellow]Interface:[/yellow] {args.interface}")
    else:
        console.print("[yellow]Interface:[/yellow] Default")

    console.print(
        f"[yellow]Filter:[/yellow] {bpf_filter if bpf_filter else 'None'}"
    )

    console.print("\n[cyan]Waiting for packets... Press CTRL+C to stop.\n")

    capture = PacketCapture(
        callback=process_packet,
        interface=args.interface,
        bpf_filter=bpf_filter,
    )

    try:
        capture.start()

    except KeyboardInterrupt:

        console.print("\n\nStopping PacketLens...")

        ReportGenerator.generate(stats)

        console.print("[green]HTML Report Generated[/green]")
        console.print("[green]CSV Export Saved[/green]")
        console.print("[green]JSON Export Saved[/green]")
        console.print("[green]PCAP Export Saved[/green]")

        console.print("\n[bold cyan]Thank you for using PacketLens![/bold cyan]\n")

    except Exception as e:
        logging.error(str(e))
        console.print(f"[red]{e}[/red]")


if __name__ == "__main__":
    main()