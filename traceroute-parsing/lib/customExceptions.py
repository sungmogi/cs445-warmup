class ExpectedTracerouteError(Exception):
    def __init__(self, key):
        self.message = f"Expected error: {key} This traceroute is same to skip since it is not valid..."
        super().__init__(self.message)


class TracerouteKeyError(Exception):
    # Raised when an error occurs while loading a traceroute
    def __init__(self, key):
        self.message = f"Missing key '{key}' in traceroute"
        super().__init__(self.message)


class TracerouteIncompleteError(Exception):
    # Raised when the status of a traceroute is not complete
    def __init__(self):
        self.message = f"Traceroute is not complete"
        super().__init__(self.message)


class TracerouteNoHopsError(Exception):
    # Raised when the there's no "hops" key in the jsonl object
    def __init__(self):
        self.message = f"No 'hops' key in traceroute"
        super().__init__(self.message)


class TracerouteProbeError(Exception):
    # Raised when the status of a traceroute is not complete
    def __init__(self):
        self.message = f"'address not allowed"
        super().__init__(self.message)


class TracerouteDNSError(Exception):
    # Raised when the status of a traceroute is not complete
    def __init__(self):
        self.message = f"name resolution failed: nodename nor servname provided or not known"
        super().__init__(self.message)


class HopUnresponsiveError(Exception):
    # Raised when a hop in a RIPE Atlas traceroute is unresponsive
    def __init__(self):
        self.message = f"Hop not responsive"
        super().__init__(self.message)


class UnknownTracerouteError(Exception):
    # Raised when a undefined error occurs while loading a traceroute
    def __init__(self):
        self.message = f"Unknown Traceroute error"
        super().__init__(self.message)

