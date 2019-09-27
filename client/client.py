import subprocess
import requests
import json
import re
from threading import Thread

import datetime

import time

start = time.time()


class GetOsCommand(Thread):

    def __init__(self, cmd):
        self.retrnData = None
        self.cmd = cmd
        super(GetOsCommand, self).__init__()

    def run(self):
        print("Getting OS command for {}".format(self.cmd))

        # Get date, decode and remove extra char return
        '''
        try:
            self.retrnData = subprocess.check_output(self.cmd).decode('UTF-8')
        except:
            pass
        '''

        self.retrnData = subprocess.run(self.cmd, capture_output=True)
        self.retrnData = self.retrnData.stdout.decode('UTF-8')
        self.retrnData = self.retrnData.replace('\r\n', '\n')


class NetdiagClient(object):

    def __init__(self, server=None, port=None):
        self.server = server
        self.port = port


    def postData(self, jsonData):
        if self.server is None:
            return "No server configured"

        serverCall = "http://{}:{}/_api/upload-diag".format(self.server, self.port)
        res = requests.post(serverCall, json = {"netData" : jsonData})

        if res.ok:
            print()


def main():

    tStamp = datetime.datetime.now().replace(microsecond=0)


    taskDict = {"systemInfo": "systeminfo",
                "trcRtPubDns": "tracert -d -w 250 -h 15 8.8.8.8",
                "trcRtOfc365": "tracert -d -w 250 -h 15 outlook.office365.com",
                "trcRtSrvcNow": "tracert -d -w 250 -h 15 tn.service-now.com",
                 "trcRtNdcDns": "tracert -d -w 250 -h 10 10.23.98.64",
                 "trcRtSdcDns": "tracert -d -w 250 -h 10 10.15.98.64",
                 "pgPubDns":"ping 8.8.8.8", "pgSdcDns":"ping 10.15.98.64",
                 "pgTnGov": "ping tn.gov", "pgNdcDns": "ping 10.23.98.64",
                 "pgOfc365": "ping outlook.office365.com",
                 "pgSrvcNow": "ping tn.service-now.com",
                 "wlanStat": "netsh wlan show interfaces",
                 "ipAdd": "ipconfig /all",
                 "topAppMem": 'tasklist /fi "memusage gt 40000"',
                 "hostName": "hostname", "userName": "whoami",
                 "wireless": "Netsh WLAN show interfaces" }



    retrnDict = {"dateUserRan": str(tStamp), "ticketNum": 0000000}
    threads = {}
    for cmdKey, cmdVal in taskDict.items():
        cmdKeyStr = cmdKey # create string before var type becomes thread

        # Instantiate thread class and start thread
        cmdKey = GetOsCommand(cmdVal,)
        cmdKey.start()

        # Add thread to dict
        threads[cmdKeyStr] = cmdKey

    # Loop over dict of threads, get data and add to dict
    for thrdKey, thrdVal in threads.items():
        thrdVal.join()
        retrnDict[thrdKey]= thrdVal.retrnData

    #for k,v in retrnDict.items():
    #   print("{}: {}".format(k, v))

    #diag = NetdiagClient("10.8.4.128", 30843)

    diag = NetdiagClient("127.0.0.1", 8443)


    diag.postData(retrnDict)

    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()


