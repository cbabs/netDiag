import os
import time
import datetime
import re
import json
from dateutil import parser
from mongodb import MongoDb




class NetDiag(object):

    def __init__(self):

        self.mDb = MongoDb()

    # Convert windows date string to ES compatible string
    def dateEsProc(self, dateStr):

        print(dateStr)

        dateUserRan = dateStr.replace("\n", "")
        dateUserRan = dateUserRan.replace("/", ":")
        dateUserRan = dateUserRan.split(".", 1)[0]

        datTimObj = datetime.datetime.strptime(dateUserRan, '%m:%d:%Y: %H:%M:%S')

        #print(datTimObj)

        return str(datTimObj)

    def dateMongoProc(self, dateStr):

        dateUserRunDtOnj = datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')

        return dateUserRunDtOnj


    def processData(self, jsonData):

        transDict = None

        tStamps = self.getTimeStamps()

        jsonData = jsonData["netData"]

        ip = jsonData["ipAdd"]

        # Dict for transaction record
        diagRecord = {
            "dateSrvImpt": tStamps["timeStmp"],
            "dateUserRan": parser.parse(jsonData["dateUserRan"]),
            "userId": jsonData["userName"].replace("\n","").replace("\\", "/"),
            "hostName": jsonData["hostName"].replace("\n",""),
            "ticketNum": jsonData["ticketNum"],
            "ipconfig": self.fltrIpInfo(ip),
            "traceGoglDns": self.fltrTracRt(jsonData["trcRtPubDns"]),
            "traceSdcDns": self.fltrTracRt(jsonData["trcRtSdcDns"]),
            "traceNdcDns": self.fltrTracRt(jsonData["trcRtNdcDns"]),
            "traceTnGov": self.fltrTracRt(jsonData["trcRtTnGov"]),
            "pingGoglDns": self.fltrPing(jsonData["pgPubDns"]),
            "pingSdcDns": self.fltrPing(jsonData["pgSdcDns"]),
            "pingNdclDns": self.fltrPing(jsonData["pgNdcDns"]),
            "pingTnGov": self.fltrPing(jsonData["pgTnGov"]),
            "procInfo": self.fltrProcInfo(jsonData["topAppMem"])
            }

        statusDict = self.createStatusDict(diagRecord)
        diagRecord["statusDict"] = statusDict
        print(diagRecord)

        self.sendTranToDbs(diagRecord)
        print(diagRecord)

    # Process ping result and gives diag hints
    def procPingStatus(self, pingDict):

        pingLoss = int(pingDict['pingLossPrct'])
        print(pingDict)

        if pingLoss == 0:
            pingLatncy = int(pingDict['latencyAvg'])
            statDict = {'Average Latency': pingLatncy}
            statDict["State"] = "OK"
            statDict["Ping Loss"] = pingLoss
        else:
            mesg = "Ping loss is high to {}.  Anything over 1-2% indicates an issue. Check basic network settings, like connection, default gateway, ".format(pingDict['ipAddr'])
            statDict ={"State": "Warning", "Ping Loss": pingLoss,
                       'Average Latency': 0, "Message": mesg}
            return statDict

        if 0 <= pingLatncy <= 120:
            statDict['Message'] = "No ping loss to {} and latency should be acceptable for voice and all other apps.".format(pingDict['ipAddr'])
        elif 121 <= pingLatncy <= 200:
            statDict['Message'] = "No ping loss to {} but latency is a little high. Voice and video may suffer.  Web, email and most other apps should be fine.".format(pingDict['ipAddr'])
        elif pingLatncy > 200:
            statDict['Message'] = "No ping loss to {} but latency is very high. Check network bandwidth, and look at traceroute and see where high latency begins".format(pingDict['ipAddr'])

        return statDict

    # Create status dict from client
    def createStatusDict(self, dataDict):

        retrnDict = {}

        # Proc ping data
        for k,v in dataDict.items():
            if re.search(r'^ping', k):
                tempDict = self.procPingStatus(v)
                retrnDict[k] = tempDict

        return retrnDict


    # Gets dict of current time stamps
    def getTimeStamps(self):

        # Create epoch
        ts = time.time()

        # Create human readable TS from epoch
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        retrnDict = {"epoch": ts, "timeStmp": st}

        return retrnDict

    # Process and return ipconfig data
    def fltrIpInfo(self, data):

        ipLines = data.splitlines() # Create array from data

        lstLength = len(ipLines) # Get list

        # Regex
        confKeyRgx = r'^(.*?)(\s\.)'
        confValRgx = r'(:\s)(.*)'

        retrnDict = [] # Dict to return data from func

        lstCnt = 0 # Index for loop count
        subConfDict = {}
        for line in ipLines:

            lstCnt += 1 # Increment loop index

            # If it last itertion append data end exit loop
            if lstCnt == lstLength:
                print("Last one")
                retrnDict.append(subConfDict)
                break

            # Skip line if empty
            if not line:
                continue

            # If line 1st char is a capital letter, create new dict
            if re.match(r'^[A-Z]', line):

                if subConfDict:
                    retrnDict.append(subConfDict)

                subConfDict = {line: {}}
                confSect = line

                continue

            # Get regex values from line
            confKey = re.match(confKeyRgx, line)
            confVal = re.search(confValRgx, line)

            # Get key without leading white space
            if confKey:
                confKey = confKey.group(1).strip()
            # Get value
            if confVal:
                confVal = confVal.group(2)

                # Process dns servers to return list as value, up to 3 servers
                if "DNS Servers" in confKey:
                    dnsValLst = []

                    # Append first dns server
                    dnsValLst.append(confVal)
                    nextDnsSrv = lstCnt # lstCnt += 1  above. Set for next line

                    # If line has capital letter(not ip addr), do nothing
                    if re.search(r'[A-Z]', ipLines[nextDnsSrv]) is None:
                        dnsValLst.append(ipLines[nextDnsSrv].strip())

                    nextDnsSrv += 1 # Check next server
                    # If line has capital letter(not ip addr), do nothing
                    if re.search(r'[A-Z]', ipLines[nextDnsSrv]) is None:
                        dnsValLst.append(ipLines[nextDnsSrv].strip())
                        subConfDict[confSect][confKey] = dnsValLst

                        continue

                    subConfDict[confSect][confKey] = dnsValLst
                    continue


            # If line empty, do nothing and exit loop
            if confKey is None: continue

            # Add kv to dict
            subConfDict[confSect][confKey] = confVal

        # Remove periods from stupid Windows ipconfig
        # Remove all periods from keys
        for confs in retrnDict:

            for k, v in confs.items():
                tempDict = {}

                # Loop all kv pairs and remove "." then add to temp dict
                for k2, v2 in v.items():
                    if "." in k2:
                        k2New = k2.replace(".", "")
                        tempDict[k2New]= v2
                    else:
                        tempDict[k2]= v2

                confs[k]= tempDict # Add temp dict to pairs


        return retrnDict

    # Process process info into list of dicts
    def fltrTracRt(self, data):

        # Regex
        regxDigts = r'[0-9*\.]+'
        regxWords = r'[a-zA-Z0-9_\.,\[\]]+'


        data = data.splitlines() # Create list from input data

        retrnDict = {"ipAddr": "", "traceList": []} # List to be returned from func

        regxIpAddr = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' # Sloppy ip addr search

        for line in data:



            if not line: continue # If line is empty, continue loop

            # Ignore lines with Trace complete and empty ones
            if "Trace complete" in line: continue
            if re.search(r'[a-z]', line) is None: continue

            wrdsLst = re.findall(regxWords, line) # List from words in line
            digtLst = re.findall(regxDigts, line) # List from words in line


            if "Tracing" in line:
                ipAddr = re.search(regxIpAddr, line)
                #print(ipAddr[0])
                retrnDict["ipAddr"] = ipAddr[0]
                continue

            if "Destination net unreachable" in line:
                lineDict = {
                "tracOrdrNum": digtLst[0],
                "trip1time": line}
                retrnDict["traceList"].append(lineDict) # Append list to be returned
                continue

            if "Transmit error" in line:
                lineDict = {
                "tracOrdrNum": digtLst[0],
                "trip1time": line}
                retrnDict["traceList"].append(lineDict) # Append list to be returned
                continue

            if "Unable to resolve" in line:
                lineDict = {
                "tracOrdrNum": digtLst[0],
                "trip1time": line}
                retrnDict["traceList"].append(lineDict) # Append list to be returned
                continue

            if "over a" in line: continue

            # Dict to append to list
            lineDict = {
                "tracOrdrNum": digtLst[0],
                "trip1time": digtLst[1],
                "trip2time": digtLst[2],
                "trip3time": digtLst[3],
                "ipAddrHop": digtLst[4]
                }

            retrnDict["traceList"].append(lineDict) # Append list to be returned

        return retrnDict


    # Process process info into list of dicts
    def fltrProcInfo(self, data):

        # Regex
        regxWords = '[a-zA-Z0-9_\.,]+'

        data = data.splitlines() # Create list from input data

        retrnLst = [] # List to be returned from func

        for line in data:

            # Only check lines with 'K' at end
            if re.search(r'K$', line):

                wrdsLst = re.findall(regxWords, line) # List from words in line

                print(line)

                # If process is Memory Compression, combine words into var
                if "Memory" in wrdsLst[0]:
                    procName = "{} {}".format(wrdsLst[0], wrdsLst[1])
                    procId = wrdsLst[2]
                else:
                    procName = wrdsLst[0]
                    procId = wrdsLst[1]

                # Create dict to append to return list
                lineDict = {
                    "proc": procName,
                    "procId": procId,
                    "session": wrdsLst[2],
                    "memory": int(wrdsLst[4].replace(",",""))
                    }

                #print(lineDict)

                retrnLst.append(lineDict) # Append list to be returned

        return retrnLst


    def fltrPing(self, data):

        # Regex
        regxDigits = r'[0-9]+' # Find digit groups
        regxIpAddr = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' # Sloppy ip search

        data = data.splitlines() # Create list from input data

        retrnDict = {} # List to be returned from func

        for line in data:

            if not line: continue # If line is empty, continue loop

            # Ignore empty lines
            if re.search(r'[a-z]', line) is None: continue

            if "Pinging" in line:
                ipAddr = re.search(regxIpAddr, line)
                retrnDict["ipAddr"] = ipAddr[0]
                continue

            if "Packets" in line:
                packtLoss = re.findall(r'[0-9]+', line)
                retrnDict["pingLossPrct"] = packtLoss[3]
                continue

            if "Minimum" in line:
                lineWords = re.findall(regxDigits, line)
                retrnDict["latencyMin"] = lineWords[0]
                retrnDict["latencyMax"] = lineWords[1]
                retrnDict["latencyAvg"] = lineWords[2]
                continue

        return retrnDict # Return dict

    # Send the transaction to DBs(ES and mongo)
    def sendTranToDbs(self, jsnData):

        mongoTrans = jsnData
        #mongoTrans['dateUserRan'] = self.dateMongoProc(mongoTrans['dateUserRan'])
        mongoTrans['dateSrvImpt'] = self.dateMongoProc(mongoTrans['dateSrvImpt'])
        #mongoTrans['ticketNum'] = int(mongoTrans['ticketNum'])
        self.mDb.addTransac(mongoTrans)


def main():

    ndiag = NetDiag("C:/workspace/TnStateDevops/netTshoot/server")

    print(ndiag.getData())

if __name__ == "__main__":
    main()