import subprocess
import requests
import json
from threading import Thread

import time

import datetime

class GetOsCommand(Thread):

    def __init__(self, cmd):
        self.retrnData = None
        self.cmd = cmd
        super(GetOsCommand, self).__init__()

    def run(self):
        #print("Getting OS command for {}".format(self.cmd))

        self.retrnData = subprocess.run(self.cmd, capture_output=True)
        self.retrnData = self.retrnData.stdout.decode('UTF-8')
        self.retrnData = self.retrnData.replace('\r\n', '\n')


class JsonFileDb(object):
    def __init__(self):

        self.reportsJson = self.readf()



    def readf(self):
        try:
            with open("data.json", "r") as test:
                test.close()
        except:
            with open("data.json", "w+") as dbFile:
                dbFile.close

        data = None
        with open("data.json", "r") as dbFile:
            readData = dbFile.read()

            if readData:
                data = json.loads(readData)

            dbFile.close()

        return data


    def write(self, dbData):
        with open("data.json", "w+") as dbFile:
            json.dump(dbData, dbFile)
            dbFile.close()

class NetdiagClient(object):

    def __init__(self, server=None, port=None):
        self.server = server
        self.port = port
        self.serverCall = "http://{}:{}/_api/upload-diag".format(server, port)

        self.db = JsonFileDb()


    def postReportDataToSvr(self, jsonData):
        if self.server is None:
            return "No server configured"

        try:
            res = requests.post(self.serverCall, json = {"netData" : jsonData})
        except Exception as e:
            print("Could not connect to server.  Saving report locally")
            self.postDataToFile(jsonData)
            print(e)
            time.sleep(5)
            return

        self.sendExistingReportsToSvr()


    def postDataToFile(self, jsonData):
        fileData = self.db.reportsJson

        if fileData:
            currentReprtList = fileData['data']
            currentReprtList.append(jsonData)
            self.db.write(fileData)
        else:
            dataDict = {"data": [jsonData]}
            self.db.write(dataDict)


    def sendExistingReportsToSvr(self):
        fileData = self.db.reportsJson

        if not fileData:
            return
        if 'data' not in fileData.keys():
            return

        print("Old reports exist. Sending to server")

        indexCnt = len(fileData['data'])

        for inx in range(len(fileData['data']), 0, -1):
            indexCnt -= 1

            print(f"Items in fileData['data]': {len(fileData['data'])}")

            print("Index: " + str(indexCnt))

            jsonData = fileData['data'][indexCnt]
            try:
                res = requests.post(self.serverCall, json = {"netData" : jsonData})
            except Exception as e:
                print(e)
                continue

            fileData['data'].pop(indexCnt) # Delete report from file


        self.db.write(fileData)




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
                 "wireless": "Netsh WLAN show interfaces",
                 "cpuLoad": "wmic cpu get loadpercentage"}


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

    diag = NetdiagClient("10.8.4.128", 30843)

    diag.postReportDataToSvr(retrnDict)


if __name__ == "__main__":
    main()


