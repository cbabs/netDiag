from Server import app
import requests
import json


# http://628205e71c04.sn.mynetname.net:9201/

class NetDiagElastic(object):

    def __init__(self):


        self.dbServers = app.config['DB_HOST']
        self.dbPort =  app.config['DB_PORT']
        self.dbIndex = app.config['DB_NAME']
        self.srv = None

        for srv in self.dbServers:

            req = r"http://{}:{}/_cluster/health?pretty".format(srv, self.dbPort)

            try:
                r = requests.get(req)

                if r.status_code == 200:
                    print('Success ' + srv)

                    self.srv = srv
                    break
            except:
                pass

        if self.srv == None:
            raise Exception("Could not connect to any ES servers")


    def getAvailSrv(self):

        print(self.srv)

    def procClntData(self, jsnData):


        pass


    def getData(self, url):

        req = r"http://{}:{}/{}".format(self.srv, self.dbPort, url)

        r = requests.get(req)
        print(r.text)

    def postData(self, url, data=None):

        urlReq = r"http://{}:{}/{}".format(self.srv, self.dbPort, url)

        if data:
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            r = requests.post(urlReq)

        print(r.text)

    def putData(self, url, data):

        url = r"http://{}:{}/{}".format(self.srv, self.dbPort, url)
        headers = {"Content-Type": "application/json"}

        print(url)

        r = requests.put(url, data=json.dumps(data), headers=headers)
        print(r.text)

    def delData(self, url):

        req = r"http://{}:{}/{}".format(self.srv, self.dbPort, url)

        r = requests.delete(req)
        print(r.text)
        print(r.status_code)

def main():

    dbSrvs = ["10.8.4.128"]

    db = NetDiagElastic(dbSrvs, 30434)



    #urlGet = r"netdiag/diag/_mapping"

    statcMappn = {
   "mappings": {
       "properties": {
         "dateUserRan": {
           "type": "date"
         }}
     }
   }

    dynMappings = {
  "mappings": {
    "diag": {
        "properties": {
         "dateUserRan": {
           "type": "date",
           "format": "yyyy-MM-dd HH:mm:ss"
         }},
      "dynamic_templates": [
        {
          "ip_addreseses": {
            "path_match": "ipAddr*",
            "mapping": {
              "type": "ip"
            }
          }
        },
        {
          "shorts": {
            "path_match": "latency*",
            "mapping": {
              "type": "short"
            }
          }
        }
      ]
    }
  }
}

    #04/14/2019:13:15:30.66

    goodInetClintDiag = {'dateSrvImpt': '2019-04-20 11:29:39', 'epochSrvImpt': 1555777779.8870053, 'dateUserRan': '2019-04-14 16:39:03', 'userId': 'ag0394v   ', 'ticketNum': '12345   ', 'ipconfig': [{'Windows IP Configuration': {'Host Name': 'DESKTOP-RGFH0PI', 'Primary Dns Suffix': '', 'Node Type': 'Peer-Peer', 'IP Routing Enabled.': 'No', 'WINS Proxy Enabled.': 'No', 'DNS Suffix Search List.': 'attlocal.net'}}, {'Ethernet adapter Ethernet:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Realtek PCIe FE Family Controller', 'Physical Address.': 'EC-8E-B5-0C-C7-B2', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter vEthernet (Default Switch):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter', 'Physical Address.': '02-15-22-9F-A0-43', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::6014:470c:d593:2cf0%3(Preferred) ', 'IPv4 Address.': '172.27.182.17(Preferred) ', 'Subnet Mask': '255.255.255.240', 'Default Gateway': '', 'DHCPv6 IAID': '872420701', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Ethernet adapter vEthernet (nat):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter #3', 'Physical Address.': '00-15-5D-92-E0-4F', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::292d:8cf7:2db4:6e76%30(Preferred) ', 'IPv4 Address.': '172.18.48.1(Preferred) ', 'Subnet Mask': '255.255.240.0', 'Default Gateway': '', 'DHCPv6 IAID': '1107301725', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #3:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #3', 'Physical Address.': '0A-00-27-00-00-24', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::b5de:6b0a:a2e6:4ad5%36(Preferred) ', 'IPv4 Address.': '192.168.211.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1208614951', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #4:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #4', 'Physical Address.': '0A-00-27-00-00-0A', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::8c29:c79c:39aa:9f98%10(Preferred) ', 'IPv4 Address.': '192.168.99.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1292501031', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Wireless LAN adapter Local Area Connection* 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter', 'Physical Address.': 'B8-81-98-2F-26-1A', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Wireless LAN adapter Local Area Connection* 3:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter #3', 'Physical Address.': 'BA-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9', 'Physical Address.': '00-FF-5C-E5-67-EA', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 5:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #2', 'Physical Address.': '00-FF-87-B7-B9-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 6:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #3', 'Physical Address.': '00-FF-F3-ED-B3-9B', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 7:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #4', 'Physical Address.': '00-FF-45-5B-CF-0D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 8:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #5', 'Physical Address.': '00-FF-E1-EE-6E-9E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 9:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #6', 'Physical Address.': '00-FF-08-0C-E4-0E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 10:': {'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #7', 'Physical Address.': '00-FF-8B-56-70-F8', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::ddd7:7061:6190:3430%21(Preferred) ', 'IPv4 Address.': '10.8.0.10(Preferred) ', 'Subnet Mask': '255.255.255.252', 'Lease Obtained.': 'Sunday, April 14, 2019 2:19:11 PM', 'Lease Expires': 'Monday, April 13, 2020 2:19:12 PM', 'Default Gateway': '10.8.0.9', 'DHCP Server': '10.8.0.9', 'DHCPv6 IAID': '1174470539', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['8.8.8.8', '4.2.2.2'], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Wireless LAN adapter Wi-Fi:': {'Connection-specific DNS Suffix': 'attlocal.net', 'Description': 'Intel(R) Dual Band Wireless-AC 3165', 'Physical Address.': 'B8-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'IPv6 Address.': '2600:1700:89c0:2da0:d4bc:5074:91d6:4edb(Preferred) ', 'Lease Obtained.': 'Sunday, April 14, 2019 2:18:43 PM', 'Lease Expires': 'Monday, April 15, 2019 4:07:33 PM', 'Temporary IPv6 Address.': '2600:1700:89c0:2da0:49e8:721d:3913:f453(Preferred) ', 'Link-local IPv6 Address': 'fe80::d4bc:5074:91d6:4edb%109(Preferred) ', 'IPv4 Address.': '192.168.1.108(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': 'fe80::eea:c9ff:fec9:ec10%109', 'DHCP Server': '192.168.1.254', 'DHCPv6 IAID': '1840808344', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['2600:1700:89c0:2da0::1', '192.168.1.254'], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Ethernet adapter Bluetooth Network Connection 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Bluetooth Device (Personal Area Network) #2', 'Physical Address.': 'B8-81-98-2F-26-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}], 'traceGoglDns': {'ipAddr': '8.8.8.8', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '77', 'trip2time': '78', 'trip3time': '78', 'ipAddrHop': '10.8.0.1'}, {'tracOrdrNum': '2', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '3', 'trip1time': '79', 'trip2time': '77', 'trip3time': '86', 'ipAddrHop': '192.168.250.253'}, {'tracOrdrNum': '4', 'trip1time': '99', 'trip2time': '99', 'trip3time': '99', 'ipAddrHop': '38.140.174.89'}, {'tracOrdrNum': '5', 'trip1time': '102', 'trip2time': '103', 'trip3time': '103', 'ipAddrHop': '154.54.31.25'}, {'tracOrdrNum': '6', 'trip1time': '99', 'trip2time': '114', 'trip3time': '100', 'ipAddrHop': '154.54.6.102'}, {'tracOrdrNum': '7', 'trip1time': '99', 'trip2time': '99', 'trip3time': '126', 'ipAddrHop': '154.54.11.226'}, {'tracOrdrNum': '8', 'trip1time': '125', 'trip2time': '115', 'trip3time': '112', 'ipAddrHop': '64.86.113.149'}, {'tracOrdrNum': '9', 'trip1time': '105', 'trip2time': '102', 'trip3time': '101', 'ipAddrHop': '64.86.113.110'}, {'tracOrdrNum': '10', 'trip1time': '108', 'trip2time': '102', 'trip3time': '104', 'ipAddrHop': '108.170.249.33'}, {'tracOrdrNum': '11', 'trip1time': '100', 'trip2time': '100', 'trip3time': '100', 'ipAddrHop': '216.239.54.129'}, {'tracOrdrNum': '12', 'trip1time': '100', 'trip2time': '100', 'trip3time': '100', 'ipAddrHop': '8.8.8.8'}]}, 'traceSdcDns': {'ipAddr': '10.15.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '77', 'trip2time': '77', 'trip3time': '77', 'ipAddrHop': '10.8.0.1'}, {'tracOrdrNum': '2', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '3', 'trip1time': '77', 'trip2time': '77', 'trip3time': '77', 'ipAddrHop': '192.168.250.253'}, {'tracOrdrNum': '4', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '5', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '6', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '7', 'trip1time': '  7     *        *     38.140.174.89  reports: Destination net unreachable.'}]}, 'traceNdcDns': {'ipAddr': '10.23.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '77', 'trip2time': '90', 'trip3time': '82', 'ipAddrHop': '10.8.0.1'}, {'tracOrdrNum': '2', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '3', 'trip1time': '80', 'trip2time': '86', 'trip3time': '81', 'ipAddrHop': '192.168.250.253'}, {'tracOrdrNum': '4', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '5', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '6', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '7', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '8', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '9', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '10', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}]}, 'traceTnGov': {'ipAddr': '170.141.221.177', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '77', 'trip2time': '78', 'trip3time': '77', 'ipAddrHop': '10.8.0.1'}, {'tracOrdrNum': '2', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipAddrHop': '.'}, {'tracOrdrNum': '3', 'trip1time': '78', 'trip2time': '88', 'trip3time': '77', 'ipAddrHop': '192.168.250.253'}, {'tracOrdrNum': '4', 'trip1time': '99', 'trip2time': '99', 'trip3time': '99', 'ipAddrHop': '38.140.174.89'}, {'tracOrdrNum': '5', 'trip1time': '104', 'trip2time': '104', 'trip3time': '102', 'ipAddrHop': '154.54.31.25'}, {'tracOrdrNum': '6', 'trip1time': '99', 'trip2time': '102', 'trip3time': '114', 'ipAddrHop': '154.54.24.250'}, {'tracOrdrNum': '7', 'trip1time': '105', 'trip2time': '134', 'trip3time': '112', 'ipAddrHop': '192.205.36.237'}, {'tracOrdrNum': '8', 'trip1time': '113', 'trip2time': '112', 'trip3time': '111', 'ipAddrHop': '12.122.117.122'}, {'tracOrdrNum': '9', 'trip1time': '110', 'trip2time': '111', 'trip3time': '112', 'ipAddrHop': '12.122.2.42'}, {'tracOrdrNum': '10', 'trip1time': '111', 'trip2time': '109', 'trip3time': '110', 'ipAddrHop': '12.122.163.129'}]}, 'pingGoglDns': {'ipAddr': '8.8.8.8', 'pingLossPrct': '0', 'latencyMin': '100', 'latencyMax': '103', 'latencyAvg': '100'}, 'pingSdcDns': {'ipAddr': '10.15.98.64', 'pingLossPrct': '100'}, 'pingNdclDns': {'ipAddr': '10.23.98.64', 'pingLossPrct': '100'}, 'pingTnGov': {'ipAddr': '170.141.221.177', 'pingLossPrct': '100'}}


    #===========================================================================
    # urlDel = r"netdiag"
    # db.delData(urlDel)
    #
    # urlPut = r"netdiag"
    # db.putData(urlPut, dynMappings)
    #
    # urlPut = r"netdiag/diag/1"
    # db.putData(urlPut, goodInetClintDiag)
    #===========================================================================


    addReplToEs = {"index" : {
        "number_of_replicas" : 1
        }
    }



    urlPut = r"graylog_*/_settings"
    db.putData(urlPut, addReplToEs)

    #db.getData(urlGet)


    noInetClientDiag = {'dateSrvImpt': '2019-04-14 13:11:26', 'epochSrvImpt': 1555265486.0635986, 'dateUserRan': '04/14/2019:12:46:49.36   ', 'userId': 'ag0394v   ', 'ticketNum': '123546   ', 'ipconfig': [{'Windows IP Configuration': {'Host Name': 'DESKTOP-RGFH0PI', 'Primary Dns Suffix': '', 'Node Type': 'Peer-Peer', 'IP Routing Enabled.': 'No', 'WINS Proxy Enabled.': 'No'}}, {'Ethernet adapter Ethernet:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Realtek PCIe FE Family Controller', 'Physical Address.': 'EC-8E-B5-0C-C7-B2', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter vEthernet (Default Switch):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter', 'Physical Address.': '02-15-22-9F-A0-43', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::6014:470c:d593:2cf0%3(Preferred) ', 'IPv4 Address.': '172.27.182.17(Preferred) ', 'Subnet Mask': '255.255.255.240', 'Default Gateway': '', 'DHCPv6 IAID': '872420701', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Ethernet adapter vEthernet (nat):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter #3', 'Physical Address.': '00-15-5D-92-E0-4F', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::292d:8cf7:2db4:6e76%30(Preferred) ', 'IPv4 Address.': '172.18.48.1(Preferred) ', 'Subnet Mask': '255.255.240.0', 'Default Gateway': '', 'DHCPv6 IAID': '1107301725', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #3:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #3', 'Physical Address.': '0A-00-27-00-00-24', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::b5de:6b0a:a2e6:4ad5%36(Preferred) ', 'IPv4 Address.': '192.168.211.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1208614951', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #4:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #4', 'Physical Address.': '0A-00-27-00-00-0A', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::8c29:c79c:39aa:9f98%10(Preferred) ', 'IPv4 Address.': '192.168.99.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1292501031', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Wireless LAN adapter Local Area Connection* 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter', 'Physical Address.': 'B8-81-98-2F-26-1A', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Wireless LAN adapter Local Area Connection* 3:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter #3', 'Physical Address.': 'BA-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9', 'Physical Address.': '00-FF-5C-E5-67-EA', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 5:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #2', 'Physical Address.': '00-FF-87-B7-B9-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 6:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #3', 'Physical Address.': '00-FF-F3-ED-B3-9B', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 7:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #4', 'Physical Address.': '00-FF-45-5B-CF-0D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 8:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #5', 'Physical Address.': '00-FF-E1-EE-6E-9E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 9:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #6', 'Physical Address.': '00-FF-08-0C-E4-0E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 10:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #7', 'Physical Address.': '00-FF-8B-56-70-F8', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Bluetooth Network Connection 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Bluetooth Device (Personal Area Network) #2', 'Physical Address.': 'B8-81-98-2F-26-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Wireless LAN adapter Wi-Fi:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': 'local.tld', 'Description': 'Intel(R) Dual Band Wireless-AC 3165', 'Physical Address.': 'B8-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}], 'traceGoglDns': {'ipAddr': '8.8.8.8', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '  1  Transmit error: code 1232.'}]}, 'traceSdcDns': {'ipAddr': '10.15.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '  1  Transmit error: code 1232.'}]}, 'traceNdcDns': {'ipAddr': '10.23.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '  1  Transmit error: code 1232.'}]}, 'traceTnGov': {'ipAddr': '', 'traceList': [{'tracOrdrNum': '.', 'trip1time': 'Unable to resolve target system name tn.gov.'}]}, 'pingGoglDns': {'ipAddr': '8.8.8.8', 'pingLossPrct': '100'}, 'pingSdcDns': {'ipAddr': '10.15.98.64', 'pingLossPrct': '100'}, 'pingNdclDns': {'ipAddr': '10.23.98.64', 'pingLossPrct': '100'}, 'pingTnGov': {}}
    goodInetClintDiag = {'dateSrvImpt': '2019-04-14 13:22:42', 'epochSrvImpt': 1555266162.3966477, 'dateUserRan': '04/14/2019:13:15:30.66   ', 'userId': 'ag0394v   ', 'ticketNum': '123456   ', 'ipconfig': [{'Windows IP Configuration': {'Host Name': 'DESKTOP-RGFH0PI', 'Primary Dns Suffix': '', 'Node Type': 'Peer-Peer', 'IP Routing Enabled.': 'No', 'WINS Proxy Enabled.': 'No'}}, {'Ethernet adapter Ethernet:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Realtek PCIe FE Family Controller', 'Physical Address.': 'EC-8E-B5-0C-C7-B2', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter vEthernet (Default Switch):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter', 'Physical Address.': '02-15-22-9F-A0-43', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::6014:470c:d593:2cf0%3(Preferred) ', 'IPv4 Address.': '172.27.182.17(Preferred) ', 'Subnet Mask': '255.255.255.240', 'Default Gateway': '', 'DHCPv6 IAID': '872420701', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Ethernet adapter vEthernet (nat):': {'Connection-specific DNS Suffix': '', 'Description': 'Hyper-V Virtual Ethernet Adapter #3', 'Physical Address.': '00-15-5D-92-E0-4F', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::292d:8cf7:2db4:6e76%30(Preferred) ', 'IPv4 Address.': '172.18.48.1(Preferred) ', 'Subnet Mask': '255.255.240.0', 'Default Gateway': '', 'DHCPv6 IAID': '1107301725', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #3:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #3', 'Physical Address.': '0A-00-27-00-00-24', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::b5de:6b0a:a2e6:4ad5%36(Preferred) ', 'IPv4 Address.': '192.168.211.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1208614951', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Ethernet adapter VirtualBox Host-Only Network #4:': {'Connection-specific DNS Suffix': '', 'Description': 'VirtualBox Host-Only Ethernet Adapter #4', 'Physical Address.': '0A-00-27-00-00-0A', 'DHCP Enabled.': 'No', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::8c29:c79c:39aa:9f98%10(Preferred) ', 'IPv4 Address.': '192.168.99.1(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Default Gateway': '', 'DHCPv6 IAID': '1292501031', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['fec0:0:0:ffff::1%1', 'fec0:0:0:ffff::2%1', 'fec0:0:0:ffff::3%1'], 'NetBIOS over Tcpip.': 'Enabled'}}, {'Wireless LAN adapter Local Area Connection* 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter', 'Physical Address.': 'B8-81-98-2F-26-1A', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Wireless LAN adapter Local Area Connection* 3:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Microsoft Wi-Fi Direct Virtual Adapter #3', 'Physical Address.': 'BA-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9', 'Physical Address.': '00-FF-5C-E5-67-EA', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 5:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #2', 'Physical Address.': '00-FF-87-B7-B9-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 6:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #3', 'Physical Address.': '00-FF-F3-ED-B3-9B', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 7:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #4', 'Physical Address.': '00-FF-45-5B-CF-0D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 8:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #5', 'Physical Address.': '00-FF-E1-EE-6E-9E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 9:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #6', 'Physical Address.': '00-FF-08-0C-E4-0E', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Ethernet adapter Ethernet 10:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'TAP-Windows Adapter V9 #7', 'Physical Address.': '00-FF-8B-56-70-F8', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}, {'Wireless LAN adapter Wi-Fi:': {'Connection-specific DNS Suffix': '', 'Description': 'Intel(R) Dual Band Wireless-AC 3165', 'Physical Address.': 'B8-81-98-2F-26-19', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes', 'Link-local IPv6 Address': 'fe80::d4bc:5074:91d6:4edb%109(Preferred) ', 'IPv4 Address.': '192.168.43.140(Preferred) ', 'Subnet Mask': '255.255.255.0', 'Lease Obtained.': 'Sunday, April 14, 2019 12:58:00 PM', 'Lease Expires': 'Sunday, April 14, 2019 1:57:59 PM', 'Default Gateway': '192.168.43.1', 'DHCP Server': '192.168.43.1', 'DHCPv6 IAID': '1840808344', 'DHCPv6 Client DUID.': '00-01-00-01-21-16-57-87-EC-8E-B5-0C-C7-B2', 'DNS Servers': ['192.168.43.1', ''], 'NetBIOS over Tcpip.': 'Disabled'}}, {'Ethernet adapter Bluetooth Network Connection 2:': {'Media State': 'Media disconnected', 'Connection-specific DNS Suffix': '', 'Description': 'Bluetooth Device (Personal Area Network) #2', 'Physical Address.': 'B8-81-98-2F-26-1D', 'DHCP Enabled.': 'Yes', 'Autoconfiguration Enabled': 'Yes'}}], 'traceGoglDns': {'ipAddr': '8.8.8.8', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '2', 'trip1time': '322', 'trip2time': '31', 'trip3time': '37', 'ipHop': '10.198.37.33'}, {'tracOrdrNum': '3', 'trip1time': '42', 'trip2time': '27', 'trip3time': '39', 'ipHop': '10.0.115.1'}, {'tracOrdrNum': '4', 'trip1time': '94', 'trip2time': '52', 'trip3time': '35', 'ipHop': '10.198.37.1'}, {'tracOrdrNum': '5', 'trip1time': '35', 'trip2time': '41', 'trip3time': '55', 'ipHop': '10.165.50.218'}, {'tracOrdrNum': '6', 'trip1time': '241', 'trip2time': '250', 'trip3time': '40', 'ipHop': '10.165.50.221'}, {'tracOrdrNum': '7', 'trip1time': '43', 'trip2time': '32', 'trip3time': '24', 'ipHop': '10.164.176.231'}, {'tracOrdrNum': '8', 'trip1time': '73', 'trip2time': '31', 'trip3time': '30', 'ipHop': '209.85.174.14'}, {'tracOrdrNum': '9', 'trip1time': '67', 'trip2time': '31', 'trip3time': '29', 'ipHop': '108.170.247.129'}, {'tracOrdrNum': '10', 'trip1time': '73', 'trip2time': '41', 'trip3time': '37', 'ipHop': '209.85.240.35'}, {'tracOrdrNum': '11', 'trip1time': '66', 'trip2time': '32', 'trip3time': '28', 'ipHop': '8.8.8.8'}]}, 'traceSdcDns': {'ipAddr': '10.15.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '11', 'trip2time': '9', 'trip3time': '3', 'ipHop': '192.168.43.1'}, {'tracOrdrNum': '2', 'trip1time': '46', 'trip2time': '30', 'trip3time': '36', 'ipHop': '10.198.37.33'}, {'tracOrdrNum': '3', 'trip1time': '50', 'trip2time': '28', 'trip3time': '28', 'ipHop': '10.0.125.1'}, {'tracOrdrNum': '4', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '5', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '6', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '7', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '8', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '9', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '10', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}]}, 'traceNdcDns': {'ipAddr': '10.23.98.64', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '13', 'trip2time': '8', 'trip3time': '6', 'ipHop': '192.168.43.1'}, {'tracOrdrNum': '2', 'trip1time': '59', 'trip2time': '29', 'trip3time': '29', 'ipHop': '10.198.37.33'}, {'tracOrdrNum': '3', 'trip1time': '56', 'trip2time': '39', 'trip3time': '58', 'ipHop': '10.0.115.1'}, {'tracOrdrNum': '4', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '5', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '6', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '7', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '8', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '9', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '10', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}]}, 'traceTnGov': {'ipAddr': '170.141.221.177', 'traceList': [{'tracOrdrNum': '1', 'trip1time': '4', 'trip2time': '5', 'trip3time': '4', 'ipHop': '192.168.43.1'}, {'tracOrdrNum': '2', 'trip1time': '72', 'trip2time': '26', 'trip3time': '29', 'ipHop': '10.198.37.33'}, {'tracOrdrNum': '3', 'trip1time': '423', 'trip2time': '44', 'trip3time': '28', 'ipHop': '10.0.115.1'}, {'tracOrdrNum': '4', 'trip1time': '83', 'trip2time': '36', 'trip3time': '33', 'ipHop': '10.198.37.1'}, {'tracOrdrNum': '5', 'trip1time': '69', 'trip2time': '29', 'trip3time': '45', 'ipHop': '10.165.50.218'}, {'tracOrdrNum': '6', 'trip1time': '40', 'trip2time': '28', 'trip3time': '26', 'ipHop': '10.165.50.221'}, {'tracOrdrNum': '7', 'trip1time': '38', 'trip2time': '28', 'trip3time': '30', 'ipHop': '10.164.176.231'}, {'tracOrdrNum': '8', 'trip1time': '68', 'trip2time': '42', 'trip3time': '27', 'ipHop': '4.71.136.21'}, {'tracOrdrNum': '9', 'trip1time': '*', 'trip2time': '*', 'trip3time': '*', 'ipHop': '.'}, {'tracOrdrNum': '10', 'trip1time': '334', 'trip2time': '130', 'trip3time': '380', 'ipHop': '4.68.62.226'}]}, 'pingGoglDns': {'ipAddr': '8.8.8.8', 'pingLossPrct': '0', 'latncyMin': '40', 'latncyMax': '496', 'latncyAvg': '199'}, 'pingSdcDns': {'ipAddr': '10.15.98.64', 'pingLossPrct': '75'}, 'pingNdclDns': {'ipAddr': '10.23.98.64', 'pingLossPrct': '100'}, 'pingTnGov': {'ipAddr': '170.141.221.177', 'pingLossPrct': '100'}}



if __name__ == "__main__":

    main()
