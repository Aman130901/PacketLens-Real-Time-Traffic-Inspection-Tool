import os
from datetime import datetime


class ReportGenerator:

    @staticmethod
    def generate(stats):

        os.makedirs("reports", exist_ok=True)

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>PacketLens Report</title>

<style>

body{{
font-family:Arial;
background:#f4f4f4;
padding:30px;
}}

table{{
border-collapse:collapse;
width:60%;
}}

th,td{{
border:1px solid #ddd;
padding:10px;
}}

th{{
background:#3498db;
color:white;
}}

</style>

</head>

<body>

<h1>PacketLens Network Report</h1>

<p>
Generated:
{datetime.now()}
</p>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr><td>Total Packets</td><td>{stats.total}</td></tr>

<tr><td>TCP</td><td>{stats.tcp}</td></tr>

<tr><td>UDP</td><td>{stats.udp}</td></tr>

<tr><td>ICMP</td><td>{stats.icmp}</td></tr>

<tr><td>ARP</td><td>{stats.arp}</td></tr>

<tr><td>Other</td><td>{stats.other}</td></tr>

</table>

</body>

</html>
"""

        with open("reports/report.html", "w") as f:
            f.write(html)

        print("\nReport generated -> reports/report.html")