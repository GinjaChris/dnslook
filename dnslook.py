#usage: python3 dnslook.py <domain or ip address>
#python3.x
import sys
import dns.resolver
import dns.reversename
import argparse
import ipaddress

parser = argparse.ArgumentParser()
parser.add_argument("destination")
args = parser.parse_args()
dest = args.destination
dnsrecords = ["A", "AAAA", "MX", "NS", "SOA", "TXT"]

#function to check if user supplied a name or an IP
def check(dest):
    try:
        if ipaddress.ip_address(dest):
            revlook(dest)
        else:
         dnslook(dest)
    except:
        dnslook(dest)

#function to perform reverse lookup (if we think an IP was supplied)
def revlook(dest):
    revdest = dns.reversename.from_address(dest)
    try:
        result = dns.resolver.resolve(revdest, "PTR")
        for val in result:
            print("PTR:", val.to_text())
    except dns.resolver.NoAnswer:
        print("PTR: No record found")
    except dns.resolver.NXDOMAIN:
        print("PTR: NXDOMAIN response")

#function to perform a forward lookup (if we think a name was supplied)
def dnslook(dest):
        for record in dnsrecords:
                try:
                        result = dns.resolver.resolve(dest, record)
                        for val in result:
                                print(record,":", val.to_text())
                except dns.resolver.NoAnswer:
                        print(record,": No record found")
                except dns.resolver.NXDOMAIN:
                        print(record,": NXDOMAIN response received")
                except dns.exception.Timeout:
                        print(record,": The request timed out!")


check(dest)

