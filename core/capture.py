from scapy.all import sniff


class PacketCapture:

    def __init__(self, callback, interface=None, bpf_filter=None):
        self.callback = callback
        self.interface = interface
        self.bpf_filter = bpf_filter

    def start(self):

        sniff(
            iface=self.interface,
            prn=self.callback,
            store=False,
            filter=self.bpf_filter
        )