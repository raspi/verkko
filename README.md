# verkko

# Usage
```
usage: main.py [global args] <subcommand> [subcommand arg(s)] <arg..>
  main.py range 192.168.0.0 192.168.0.255
  main.py ip 192.168.1.1
  main.py nw 192.168.0.0/24

positional arguments:
  {nw,ip,range}  commands
    nw           Get information about a given IP network. Example:
                 192.168.0.0/24
    ip           Get information about a given IP address. Example:
                 192.168.1.1
    range        Generate IP network from two IP addresses. Example:
                 192.168.0.0 192.168.0.255

optional arguments:
  -h, --help     show this help message and exit
```

# Example IP:

```
% python main.py ip ::1:2:3:4
           Exploded:  0000:0000:0000:0000:0001:0002:0003:0004   0000:0000:0000:0000:0001:0002:0003:0004
                      0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000001:0000000000000010:0000000000000011:0000000000000100
         Compressed:  ::1:2:3:4   0000:0000:0000:0000:0001:0002:0003:0004
                      0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000001:0000000000000010:0000000000000011:0000000000000100
  Max prefix length:  128   0x80   0b10000000
        Reverse PTR:  4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa
         IP version:  6

Is:
  Global: True  Private: False  Reserved: True  Loopback: False  Multicast: False  Link local: False  Unspecified: False
```

# Example network:

```
% python main.py nw 2002:7f00::/24
    Network address:  2002:7f00::   2002:7f00:0000:0000:0000:0000:0000:0000
                      0010000000000010:0111111100000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000
              First:  2002:7f00::1   2002:7f00:0000:0000:0000:0000:0000:0001
                      0010000000000010:0111111100000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000001
               Last:  2002:7fff:ffff:ffff:ffff:ffff:ffff:fffe   2002:7fff:ffff:ffff:ffff:ffff:ffff:fffe
                      0010000000000010:0111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111110
          Broadcast:  2002:7fff:ffff:ffff:ffff:ffff:ffff:ffff  2002:7fff:ffff:ffff:ffff:ffff:ffff:ffff
                      0010000000000010:0111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111
            Netmask:  ffff:ff00::  ffff:ff00:0000:0000:0000:0000:0000:0000
                      1111111111111111:1111111100000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000
           Hostmask:  0:ff:ffff:ffff:ffff:ffff:ffff:ffff  0000:00ff:ffff:ffff:ffff:ffff:ffff:ffff
                      0000000000000000:0000000011111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111:1111111111111111
           Exploded:  2002:7f00:0000:0000:0000:0000:0000:0000/24
         Compressed:  2002:7f00::/24
      Prefix length:  24   0x18   0b11000
  Max prefix length:  128   0x80   0b10000000
Number of addresses:  20,282,409,603,651,670,423,947,251,286,016   0x100000000000000000000000000   0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        Reverse PTR:  4.2./.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.f.7.2.0.0.2.ip6.arpa
         IP version:  6

With:
   Hostmask: 2002:7f00::/0:ff:ffff:ffff:ffff:ffff:ffff:ffff
    Netmask: 2002:7f00::/ffff:ff00::
  Prefixlen: 2002:7f00::/24
Is:
  Global: True  Private: False  Reserved: False  Loopback: False  Multicast: False  Link local: False  Unspecified: False
```

# Example range:

```
% python main.py range 192.168.0.1 192.168.1.128
192.168.0.1/32   192.168.0.1 - 192.168.0.1 with 1 address(es)
192.168.0.2/31   192.168.0.2 - 192.168.0.3 with 2 address(es)
192.168.0.4/30   192.168.0.4 - 192.168.0.7 with 4 address(es)
192.168.0.8/29   192.168.0.8 - 192.168.0.15 with 8 address(es)
192.168.0.16/28   192.168.0.16 - 192.168.0.31 with 16 address(es)
192.168.0.32/27   192.168.0.32 - 192.168.0.63 with 32 address(es)
192.168.0.64/26   192.168.0.64 - 192.168.0.127 with 64 address(es)
192.168.0.128/25   192.168.0.128 - 192.168.0.255 with 128 address(es)
192.168.1.0/25   192.168.1.0 - 192.168.1.127 with 128 address(es)
192.168.1.128/32   192.168.1.128 - 192.168.1.128 with 1 address(es)
```
