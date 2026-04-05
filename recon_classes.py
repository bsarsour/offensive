import os
import subprocess
import nmap3

class IpAddres:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac
        self.subnet = ""
        self.services = []
        
    def show_ip(self):
        print(self.ip)

class AliveScan:
    def __init__(self, ip_network, ip_subnet):
        self.ip_network = ip_network
        self.ip_subnet = ip_subnet
        self.res = self.run_arp_scan()

    def run_arp_scan(self):
        ip_address_list = []
        alive_command = ["arp-scan", f"{self.ip_network}/{self.ip_subnet}", "-q"]
        res = subprocess.run(alive_command, encoding='utf-8', capture_output=True)
        res_list = max(res.stdout.split(" "), key=len)
        ip_mac = bytes(res_list.encode()).decode().split("\n")
        for x in ip_mac:
            if b"\t" in x.encode():
                ip_address_list.append({
                    "ip_address" : x.split("\t")[0],
                    "mac_address" : x.split("\t")[-1]
                    })
        return ip_address_list

class PortScan:
    def __init__(self, ip):
        self.ip = ip
        self.res = self.port_scan()

    def port_scan(self):
        nmap = nmap3.Nmap()
        results = nmap.nmap_version_detection(self.ip)#, args="-p-")
        detected_services = []
        for open_port in results[self.ip]["ports"]:
            try:
                port_data = {
                    "port" : open_port['portid'],
                    "name" : open_port['service']['name'],
                    "service" : f"{open_port['service']['product']}{open_port['service']['version']}"
                }
                detected_services.append(port_data)
            except KeyError:
                continue
        return detected_services

class ServiceEnum:
    ...



if os.getuid() != 0:
    print("must run as root")
    exit(0)

ip_network = "192.168.2.0"
ip_subnet = "24"
arp_scan = AliveScan(ip_network, ip_subnet)
ip_address_obj = []
for res in arp_scan.res:
    ip_address_obj.append(IpAddres(res['ip_address'], res['mac_address']))

for obj in ip_address_obj:
    print(f"scan: {obj.ip}", end="\r")
    for res in PortScan(obj.ip).res:
        obj.services.append(res)

for i in ip_address_obj:
    print(f"ip::{i.ip}\t mac::{i.mac} \n services::{i.services}")

