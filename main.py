import argparse
import ipaddress
import logging
import os
import sys
from collections.abc import Iterable


def chunks(lst: Iterable, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def to_bin(b: ipaddress._IPAddressBase) -> str:
    if isinstance(b, ipaddress.IPv4Address):
        l: list = list(map(int, b.packed))
        return ".".join(map(lambda x: "{0:b}".format(x).zfill(8), l))
    elif isinstance(b, ipaddress.IPv6Address):
        return ":".join(chunks(bin(int(b))[2:].zfill(128), 16))


def to_hex(b: ipaddress._IPAddressBase) -> str:
    if isinstance(b, ipaddress.IPv4Address):
        l: list = list(map(int, b.packed))
        return ".".join(map(lambda x: "{0:x}".format(x).zfill(2), l))
    elif isinstance(b, ipaddress.IPv6Address):
        return b.exploded


if __name__ == '__main__':

    THIS = os.path.basename(sys.argv[0])
    EXAMPLES = [
        f"{THIS} range 192.168.0.0 192.168.0.255",
        f"{THIS} ip 192.168.1.1",
        f"{THIS} nw 192.168.0.0/24",
    ]

    log = logging.getLogger(__name__)

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        stream=sys.stdout,
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(
        usage=f'{THIS} [global args] <subcommand> [subcommand arg(s)] <arg..>' +
              "\n  " +
              "\n  ".join(EXAMPLES),
        epilog='',
    )
    subparsers = parser.add_subparsers(
        dest="subparser_name",
        help='commands',
    )

    network_parser = subparsers.add_parser(
        'nw',
        usage='<IPv4 or IPv6 network>',
        help='Get information about a given IP network. Example: 192.168.0.0/24',
    )
    ip_parser = subparsers.add_parser(
        'ip',
        usage='<IPv4 or IPv6 address>',
        help='Get information about a given IP address. Example: 192.168.1.1',
    )
    range_parser = subparsers.add_parser(
        'range',
        usage='<IPv4 or IPv6 address> <IPv4 or IPv6 address>',
        help='Generate IP network from two IP addresses. Example: 192.168.0.0 192.168.0.255',
    )

    args = parser.parse_known_args()
    subparser_name: str = args[0].subparser_name

    if subparser_name == 'nw':
        """
        Network
        """
        scargs = network_parser.parse_known_args(args[1])
        arg = scargs[1]
        if len(arg) == 0:
            print(f"See: {os.path.basename(sys.argv[0])} {subparser_name} --help")
            sys.exit(0)

        net: ipaddress._BaseNetwork
        try:
            net = ipaddress.ip_network(arg[0])
        except ValueError as e:
            print(f"{arg}? {e}", file=sys.stderr)
            sys.exit(1)

        if not (isinstance(net, ipaddress.IPv6Network) or isinstance(net, ipaddress.IPv4Network)):
            print(f"wot is {arg}?", file=sys.stderr)
            sys.exit(1)

        first: ipaddress._IPAddressBase = net.network_address
        last: ipaddress._IPAddressBase = net.broadcast_address

        if isinstance(net, ipaddress.IPv6Network) and net.prefixlen != 128:
            first += 1
            last -= 1
        elif isinstance(net, ipaddress.IPv4Network) and net.prefixlen != 32:
            first += 1
            last -= 1

        print(f"    Network address:  {net.network_address}   {to_hex(net.network_address)}")
        print(f"                      {to_bin(net.network_address)}")
        print(f"              First:  {first}   {to_hex(first)}")
        print(f"                      {to_bin(first)}")
        print(f"               Last:  {last}   {to_hex(last)}")
        print(f"                      {to_bin(last)}")
        print(f"          Broadcast:  {net.broadcast_address}  {to_hex(net.broadcast_address)}")
        print(f"                      {to_bin(net.broadcast_address)}")
        print(f"            Netmask:  {net.netmask}  {to_hex(net.netmask)}")
        print(f"                      {to_bin(net.netmask)}")
        print(f"           Hostmask:  {net.hostmask}  {to_hex(net.hostmask)}")
        print(f"                      {to_bin(net.hostmask)}")
        print(f"           Exploded:  {net.exploded}")
        print(f"         Compressed:  {net.compressed}")
        print(f"      Prefix length:  {net.prefixlen}   0x{net.prefixlen:2x}   0b{net.prefixlen:b}")
        print(f"  Max prefix length:  {net.max_prefixlen:,}   0x{net.max_prefixlen:2x}   0b{net.max_prefixlen:b}")
        print(f"Number of addresses:  {net.num_addresses:,}   0x{net.num_addresses:2x}   0b{net.num_addresses:b}")
        print(f"        Reverse PTR:  {net.reverse_pointer}")
        print(f"         IP version:  {net.version}")

        print()
        print(f"With:")
        print(f"   Hostmask: {net.with_hostmask}")
        print(f"    Netmask: {net.with_netmask}")
        print(f"  Prefixlen: {net.with_prefixlen}")
        print(f"Is:")
        print(
            f"  Global: {net.is_global}"
            f"  Private: {net.is_private}"
            f"  Reserved: {net.is_reserved}"
            f"  Loopback: {net.is_loopback}"
            f"  Multicast: {net.is_multicast}"
            f"  Link local: {net.is_link_local}"
            f"  Unspecified: {net.is_unspecified}"
        )
    elif subparser_name == 'range':
        """
        IP Address range
        """
        scargs = range_parser.parse_known_args(args[1])
        arg = scargs[1]
        if len(arg) == 0:
            print(f"See: {os.path.basename(sys.argv[0])} {subparser_name} --help")
            sys.exit(0)

        addr1: ipaddress._BaseAddress
        addr2: ipaddress._BaseAddress

        try:
            addr1 = ipaddress.ip_address(arg[0])
            addr2 = ipaddress.ip_address(arg[1])
        except ValueError as e:
            print(f"wot is {arg}?", file=sys.stderr)
            sys.exit(1)
        for i in ipaddress.summarize_address_range(addr1, addr2):
            print(i)
    elif subparser_name == 'ip':
        """
        IP Address
        """
        scargs = ip_parser.parse_known_args(args[1])
        arg = scargs[1]

        if len(arg) == 0:
            print(f"See: {os.path.basename(sys.argv[0])} {subparser_name} --help")
            sys.exit(0)

        addr: ipaddress._BaseAddress

        try:
            addr = ipaddress.ip_address(arg[0])
        except ValueError as e:
            print(f"wot is {arg}?", file=sys.stderr)
            sys.exit(1)

        print(f"           Exploded:  {addr.exploded}   {to_hex(addr)}")
        print(f"                      {to_bin(addr)}")
        print(f"         Compressed:  {addr.compressed}   {to_hex(addr)}")
        print(f"                      {to_bin(addr)}")
        print(f"  Max prefix length:  {addr.max_prefixlen:,}   0x{addr.max_prefixlen:2x}   0b{addr.max_prefixlen:b}")
        print(f"        Reverse PTR:  {addr.reverse_pointer}")
        print(f"         IP version:  {addr.version}")

        print()
        print(f"Is:")
        print(
            f"  Global: {addr.is_global}"
            f"  Private: {addr.is_private}"
            f"  Reserved: {addr.is_reserved}"
            f"  Loopback: {addr.is_loopback}"
            f"  Multicast: {addr.is_multicast}"
            f"  Link local: {addr.is_link_local}"
            f"  Unspecified: {addr.is_unspecified}"
        )
