import json
from lib.customExceptions import *


class Hop:
    def __init__(self, hop_data, ip_data=None, bdrmapit_data=None):
        self.addr = self._get_addr_from_hop(hop_data)
        self.rtt = self._get_rtt_from_hop(hop_data)
        self.rtt_backup = self.rtt
        self.fixed_rtt = False

        self.asn = None
        self.bdrmapit_asn = None
        self.asn_org = None
        self.bdrmapit_asn_org = None
        self.asn_name = None
        self.bdrmapit_asn_name = None
        self.rdns = None
        self.coords = None
        self.geoloc = None
        self.shift = False

        self.is_bogon = False

        if ip_data is not None:
            self._parse_ip_data(ip_data)

        if bdrmapit_data is not None:
            self._parse_bdrmapit_data(bdrmapit_data)

    def _parse_ip_data(self, ip_data):
        self.rdns = ip_data.get("rdns", None)
        self.coords = ip_data.get("coords", None)
        self.asn = ip_data.get("asn", "*")
        self.asn_org = ip_data.get("asn_org", None)
        self.asn_name = ip_data.get("asn_name", None)

        self.geoloc = ip_data.get("geoloc", None)
        if (not self.geoloc.country) or (self.geoloc.country is None):
            self.geoloc = None

    def _parse_bdrmapit_data(self, bdrmapit_data):
        self.bdrmapit_asn = bdrmapit_data.get("asn", None)
        self.bdrmapit_asn_org = bdrmapit_data.get("asn_org", None)
        self.bdrmapit_asn_name = bdrmapit_data.get("asn_name", None)

    def _get_addr_from_hop(self, hop_data):
        raise NotImplementedError

    def _get_rtt_from_hop(self, hop_data):
        raise NotImplementedError

    def _get_asn_str(self):
        if self.is_bogon:
            return "b"
        elif isinstance(self.bdrmapit_asn, int) and not isinstance(self.asn, int):
            return f"{self.bdrmapit_asn}(bdrmapit)"
        elif (isinstance(self.asn, int) and not isinstance(self.bdrmapit_asn, int)) or (
            isinstance(self.asn, int)
            and isinstance(self.bdrmapit_asn, int)
            and self.asn == self.bdrmapit_asn
        ):
            return f"{self.asn}"
        elif (
            isinstance(self.asn, int)
            and isinstance(self.bdrmapit_asn, int)
            and self.asn != self.bdrmapit_asn
        ):
            return f"{self.asn}/{self.bdrmapit_asn}"
        else:
            return "*"

    def _get_asn_org_str(self):
        if self.is_bogon:
            return "b"
        elif (
            isinstance(self.asn, int)
            and isinstance(self.bdrmapit_asn, int)
            and self.asn != self.bdrmapit_asn
        ):
            return f"{self.asn_org}/{self.bdrmapit_asn_org}"
        elif self.asn_org is not None:
            return self.asn_org
        elif self.bdrmapit_asn_org is not None:
            return self.bdrmapit_asn_org
        else:
            return "*"

    def get_asn(self):
        if self.is_bogon:
            return "b"
        elif isinstance(self.asn, int):
            return self.asn
        else:
            return "*"

    def set_shift(self, value):
        self.shift = value

    def __str__(self):
        locstr = (
            f"({self.geoloc.city}, {self.geoloc.state}, {self.geoloc.country})"
            if self.geoloc is not None
            else "***"
        )
        rdnsstr = self.rdns if self.rdns is not None else "*"
        # asnstr = self.asn if isinstance(self.asn, int) else '*'
        bk_rtt_str_len = len(str(self.rtt_backup))
        asnstr = self._get_asn_str()
        # asn_name = self.asn_name if self.asn_name is not None else ''
        # asn_org = f"({self.asn_org if self.asn_org is not None else ''})"
        asn_org = self._get_asn_org_str()

        if self.fixed_rtt:
            rtt_str = f"{self.rtt} ({self.rtt_backup})"
            rtt_str_len = 10 - bk_rtt_str_len + 3

            # # # Correct format string
            # return f' {self.addr:<16}{asnstr:<8}{asn_org:<50}{rtt_str:<{rtt_str_len}}{locstr:>40} {rdnsstr:<100}'
            # # return f' {self.addr:<16}{asnstr:<8}{asn_org:<50}{f"{self.rtt} ({self.rtt_backup})":<{10-bk_rtt_str_len+3}}{locstr:>40} {rdnsstr:<100}'
        # return f' {self.addr:<16}{asnstr:<8}{asn_org:<100}{self.rtt:<10}{locstr:>40} {rdnsstr:<100}'
        return f" {self.addr:<16}{asnstr:<14}{asn_org:<96}{self.rtt:<10}{locstr:>40} {rdnsstr:<100}"

    def __repr__(self):
        return self.__str__()


class RIPEHop(Hop):
    def _get_addr_from_hop(self, hop_data):
        try:
            if hop_data["from"] is None:
                import pprint

                pprint.pprint(hop_data)
                input()

            return hop_data["from"]
        except KeyError:
            raise UnknownTracerouteError()

    def _get_rtt_from_hop(self, hop_data):
        try:
            if hop_data["rtt"] == "*":
                return float("-inf")
            return float(hop_data["rtt"])
        except KeyError:
            raise UnknownTracerouteError()


class Traceroute:
    def __init__(
        self,
        data,
        conn=None,
        naive=False,
        skip_incomplete=False,
        geo_plugin=None,
        bdrmapit_map=None,
    ):
        """Attributes that are inherit to all Traceroute objects"""
        self.src = None
        self.dst = None
        self.src_asn = None
        self.dst_asn = None
        self.hops = None
        self.links = []

        self.original_json_data = data

        """ Attributes that are loaded only if the plugin functions are called """
        self.s_coords = None
        self.d_coords = None

        """ Optional attributes """
        self.status = None
        self.naive = naive
        self.skip_incomplete = skip_incomplete
        self.bdrmapit_map = bdrmapit_map

        """ Functions """

        self.SPLIT_THRESHOLD = 6.5
        self.ANOMALY_THRESHOLD = 1.5

        # self.data = data

        self._setup(data)

    def _setup(self):
        raise NotImplementedError

    def _load_hops(self):
        raise NotImplementedError

    def _set_src_dst_coords(self):
        set_src = True
        for hop in self.hops:
            if hop.geoloc is None:
                continue
            if set_src:
                self.s_coords = hop.coords
                set_src = False
            else:
                self.d_coords = hop.coords

    def __str__(self):
        rtn = []
        for hop in self.hops:
            rtn.append(f"  {str(hop)}")

        for link in self.links:
            linkStr = (
                f"{link.type} ({link.left_hop.asn})"
                if (link.left_hop.asn == link.right_hop.asn)
                else f"{link.type} ({link.left_hop.asn}, {link.right_hop.asn})"
            )
            infraStr = link.infra_stringify()
            linkStr = f"{linkStr}  {infraStr}"

            frontSymbol = "├─" if rtn[link.left_idx].startswith("╰─") else "╭─"
            rtn[link.left_idx] = f"{frontSymbol}{str(link.left_hop)}\n{linkStr}"
            rtn[link.right_idx] = f"╰─{str(link.right_hop)}"

            # rtn[link.left_idx] = f"{frontSymbol}{str(link.left_hop)}"
            # rtn[link.right_idx] = f"{linkStr}\n╰─{str(link.right_hop)}"

            for non_responsive_hop in link.non_responsive_idxs:
                rtn[non_responsive_hop] = f"├ {str(self.hops[non_responsive_hop])}"

        return "\n".join(rtn)


class RIPETraceroute(Traceroute):
    def __init__(self, data, conn=None, *args, **kwargs):
        super().__init__(data, conn=conn, *args, **kwargs)

    def _setup(self, data):
        try:
            if not self.naive:
                if "src_addr" not in data:
                    raise TracerouteProbeError()
                if "dst_addr" not in data:
                    raise TracerouteDNSError()

            self.src = data["from"] if "from" in data else data["src_addr"]
            self.dst = data["dst_addr"]
            self.probe_id = data["prb_id"]
            self.start_time = data["timestamp"]
            self.end_time = data["endtime"]
            self.hops = self._load_hops(data)

            # self.plugin_is_bogon(self.hops)

        except (
            KeyError
        ) as err:  # Traceroute is either not completed or has incomplete information
            raise TracerouteKeyError(str(err))

        # excepted errors caught when parsing raw traceroute json data
        except (
            TracerouteIncompleteError,
            TracerouteProbeError,
            TracerouteDNSError,
        ) as err:
            raise ExpectedTracerouteError(str(err))

        except Exception as error:  # Other undefined errors
            raise error
            # raise UnknownTracerouteError()

    def _load_hops(self, data):
        # Add source address to list of address to be geolocated
        addrs = [self.src]
        addr_to_hop = {self.src: {"from": self.src, "rtt": 0.000}}
        ip_data_dict = {}

        for h in data["result"]:
            if "error" in set(h.keys()):
                raise TracerouteIncompleteError()

            hop_n, h_3 = h["hop"], h["result"]  # three measurements per hop
            # sanity check
            h3_keys = [key for _h in h_3 for key in _h.keys()]
            if "error" in h3_keys:
                continue
            addr, _h = self._parse_h3_dict(h_3)

            # sometimes we get the same address for different hops, in this case we skip the hop
            # if addr in addrs: continue

            addrs.append(addr)
            addr_to_hop[addr] = _h

        _addr_lookup_list = [_addr for _addr in addrs if _addr != "*"]
        if (self.naive) or (not _addr_lookup_list):
            ip_data_dict = {}
            bdrmapit_map = {}
        else:
            ip_data_dict = {}
            bdrmapit_map = self.bdrmapit_map if self.bdrmapit_map is not None else {}

        return [
            RIPEHop(
                addr_to_hop[addr],
                ip_data=ip_data_dict.get(addr, None),
                bdrmapit_data=bdrmapit_map.get(addr, None),
            )
            for addr in addrs
        ]

    def _parse_h3_dict(self, h3):
        # Case 1: all three measurements are unresponsive or late
        if all([("x" in _h and _h["x"] == "*") or ("late" in _h) for _h in h3]):
            addr, hop = "*", {"from": "***", "rtt": "*", "size": "*", "ttl": "*"}

        # Case 2: all three measurements are responsive
        elif all([("from" in _h) and ("rtt" in _h) for _h in h3]):

            # 2024.10.19
            # We select only the first measurement for now
            addr, hop = h3[0]["from"], h3[0]

        # Case 3: at least one measurement is responsive
        elif any(("from" in _h) and ("rtt" in _h) for _h in h3):
            _h3 = [_h for _h in h3 if ("from" in _h) and ("rtt" in _h)]
            # get hop with the minimum rtt
            min_rtt_hop = min(_h3, key=lambda d: d["rtt"])
            addr, hop = min_rtt_hop["from"], min_rtt_hop
        else:
            raise UnknownTracerouteError()
        return addr, hop
