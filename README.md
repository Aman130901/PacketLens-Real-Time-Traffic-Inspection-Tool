# 📡 PacketLens — Real-Time Traffic Inspection Tool

**PacketLens** is a real-time, terminal-based network traffic inspector built in Python. It captures live packets, decodes them across multiple protocol layers, and displays a continuously updating dashboard while simultaneously exporting every packet to CSV, JSON, and PCAP for later analysis.

Where tools like Wireshark offer deep, GUI-driven inspection, PacketLens focuses on being fast, scriptable, and terminal-native ideal for quick diagnostics, learning how packet decoding works, or as a foundation for custom traffic-analysis tooling.

---

## ✨ Features

- **Live packet capture** on any interface, powered by Scapy
- **Multi-layer packet decoding** — Ethernet, ARP, IPv4, TCP, UDP, ICMP, and DNS
- **Real-time terminal dashboard** with live protocol counters and a rolling history of recent packets
- **BPF-style capture filters** — restrict capture to TCP, UDP, ICMP, ARP, or a specific port
- **Simultaneous multi-format export**:
  - `exports/packets.csv` — structured, spreadsheet-friendly log
  - `exports/packets.json` — structured JSON for programmatic use
  - `exports/capture.pcap` — full packet capture, replayable in Wireshark/tcpdump
- **Automatic HTML report** generated on exit, summarizing the session's traffic
- **Session logging** to `logs/packetlens.log` for auditing and debugging

---

## 🏗️ Architecture

PacketLens is organized as a linear capture-to-export pipeline, with each stage handled by a dedicated module:

```
 Network Interface
        │
        ▼
 ┌────────────────┐
 │ PacketCapture   │  (core/capture.py)    – live sniffing via Scapy, optional BPF filter
 └───────┬────────┘
         ▼
 ┌────────────────┐
 │ PacketDecoder   │  (core/decoder.py)    – parses Ethernet/ARP/IP/TCP/UDP/ICMP/DNS layers
 └───────┬────────┘
         ▼
 ┌────────────────┐
 │ PacketStatistics│  (core/statistics.py) – running counters + rolling packet history
 └───────┬────────┘
         ▼
 ┌───────────────────────────────┐
 │ Dashboard      │  PacketExporter │  (core/dashboard.py, core/exporter.py)
 │ (live terminal)│ (CSV/JSON/PCAP) │
 └───────────────────────────────┘
         ▼
 ┌────────────────┐
 │ ReportGenerator │  (core/report.py)     – writes reports/report.html on exit
 └────────────────┘
```

Each component is self-contained, making it straightforward to add new protocol decoders, additional export formats, or an alternate UI without disrupting the rest of the pipeline.

---

## 📁 Project Structure

```
PacketLens-Real-Time-Traffic-Inspection-Tool/
├── main.py                  # Entry point — argument parsing & capture loop
├── requirements.txt         # Python dependencies
├── config/
│   └── settings.py          # Interface, export paths, export toggles, packet cap
├── core/
│   ├── capture.py            # Live packet capture (Scapy) with BPF filter support
│   ├── decoder.py             # Multi-layer packet decoding
│   ├── statistics.py          # Live counters & rolling packet history
│   ├── dashboard.py            # Rich-based live dashboard rendering
│   ├── exporter.py             # CSV / JSON / PCAP export
│   ├── report.py               # HTML report generation
│   ├── filters.py              # Reserved for custom filter logic
│   └── utils.py                 # Reserved for shared helper utilities
├── exports/                  # Generated at runtime (packets.csv, packets.json, capture.pcap)
├── logs/                     # Generated at runtime (packetlens.log)
└── reports/                  # Generated at runtime (report.html)
```

---

## ⚙️ Requirements

- Python 3.9+
- Root/administrator privileges (required for live packet capture)
- A supported network interface

Dependencies (see `requirements.txt`):

- [`scapy`](https://pypi.org/project/scapy/) — packet sniffing and decoding
- [`rich`](https://pypi.org/project/rich/) — live terminal dashboard rendering

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/PacketLens-Real-Time-Traffic-Inspection-Tool.git
cd PacketLens-Real-Time-Traffic-Inspection-Tool

# (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Linux users:** Scapy requires elevated privileges to sniff packets. Run with `sudo`, or grant the appropriate packet-capture capabilities to your Python interpreter.

---

## ▶️ Usage

Run PacketLens on the default interface, capturing all traffic:

```bash
sudo python3 main.py
```

Capture on a specific interface:

```bash
sudo python3 main.py --interface eth0
```

Restrict capture with a protocol filter:

```bash
sudo python3 main.py --tcp        # TCP traffic only
sudo python3 main.py --udp        # UDP traffic only
sudo python3 main.py --icmp       # ICMP traffic only
sudo python3 main.py --arp        # ARP traffic only
sudo python3 main.py --port 443   # Traffic on a specific port
```

While running, the terminal refreshes with:

- **Live Dashboard** — total packet count, per-protocol breakdown (TCP/UDP/ICMP/ARP/Other), and the most recent source/destination/protocol
- **Recent Packets table** — the last 10 packets, showing protocol, source, destination, port, and any resolved DNS query

Press **`CTRL+C`** to stop capturing. On exit, PacketLens automatically:

1. Generates an HTML summary report at `reports/report.html`
2. Confirms that CSV, JSON, and PCAP exports have been saved

---

## 📤 Exports

Every captured packet is written in real time to three formats simultaneously:

| File | Format | Use Case |
|---|---|---|
| `exports/packets.csv` | CSV | Quick viewing in Excel/Sheets, spreadsheet analysis |
| `exports/packets.json` | JSON | Programmatic processing, integration with other tools |
| `exports/capture.pcap` | PCAP | Full-fidelity replay/analysis in Wireshark or tcpdump |

Export behavior (paths, enable/disable toggles) is controlled via `config/settings.py`.

---

## 🛠️ Configuration

Runtime behavior is centralized in `config/settings.py`:

```python
INTERFACE = None                       # Default network interface (None = auto)

CSV_EXPORT = "exports/packets.csv"
JSON_EXPORT = "exports/packets.json"

ENABLE_CSV = True
ENABLE_JSON = True

MAX_PACKETS = 10000                    # Session packet cap
```

---

## 🗺️ Roadmap Ideas

- Implement `core/filters.py` for advanced, composable capture filters beyond basic BPF strings
- Populate `core/utils.py` with shared helpers (e.g. IP/port formatting, protocol name resolution)
- Add live bandwidth/throughput graphs to the dashboard
- Support saving/loading capture sessions for offline replay and re-analysis
- Optional web-based dashboard alongside the terminal UI

---

## ⚠️ Disclaimer

PacketLens is intended for educational use and for inspecting networks you own or are authorized to monitor. Capturing traffic on networks without permission may be illegal in your jurisdiction. Use responsibly.

---

## 👤 Author

**Aman Sonkar**
