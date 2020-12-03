import os
import time
import datetime
import re
import json
from dateutil import parser
from mongodb import MongoDb

'''
class RabbitMq(object):
    def __init__(self):
        
        
        self.queue_receive = "recv_cmds_queue"
        self.queue_reply_cmds = "reply_cmds_queue"
        
        asyncio.ensure_future(self.start_rabbit_consumer())
        
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


    async def process_rabbit_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            messageStr = str(message.body.decode())
            messageStr = messageStr.replace("'",'"')
            messageJson = ast.literal_eval(messageStr)
            for k,v in messageJson.items():
                await self.sendCmdsToClient(k,v)


    async def send_rabbit_message(self, sendingMsg, routing_key):
        connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/")

        async with connection:
            channel = await connection.channel()

            # Declaring queue
            queue = await channel.declare_queue(self.queue_receive,
                                                auto_delete=True)

            await channel.default_exchange.publish(
            aio_pika.Message(body=sendingMsg.encode()),
            routing_key=self.queue_reply_cmds)


    async def start_rabbit_consumer(self):
        connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/")

        # Creating channel
        channel = await connection.channel()

        # Maximum message count which will be
        # processing at the same time.
        await channel.set_qos(prefetch_count=100)

        # Declaring queue
        queue = await channel.declare_queue(self.queue_reply_cmds,
                                            auto_delete=True)

        # Send message to func
        await queue.consume(self.process_rabbit_message)
'''

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

        print(jsonData["wireless"])

        # Dict for transaction record
        diagRecord = {
            "dateSrvImpt": tStamps["timeStmp"],
            "dateUserRan": parser.parse(jsonData["dateUserRan"]),
            "userId": jsonData["userName"].replace("\n","").replace("\\", "/"),
            "hostName": jsonData["hostName"].replace("\n",""),
            "ticketNum": jsonData["ticketNum"],
            "systemInfo": self.procSysInfo(jsonData["systemInfo"]),
            "ipconfig": self.fltrIpInfo(jsonData["ipAdd"]),
            "traceGoglDns": self.fltrTracRt(jsonData["trcRtPubDns"]),
            "traceOfc365": self.fltrTracRt(jsonData["trcRtOfc365"]),
            "traceSrvcNow": self.fltrTracRt(jsonData["trcRtSrvcNow"]),
            "traceSdcDns": self.fltrTracRt(jsonData["trcRtSdcDns"]),
            "traceNdcDns": self.fltrTracRt(jsonData["trcRtNdcDns"]),
            "pingGoglDns": self.fltrPing(jsonData["pgPubDns"]),
            "pingOfc365": self.fltrPing(jsonData["pgOfc365"]),
            "pingSrvcNow": self.fltrPing(jsonData["pgSrvcNow"]),
            "pingSdcDns": self.fltrPing(jsonData["pgSdcDns"]),
            "pingNdclDns": self.fltrPing(jsonData["pgNdcDns"]),
            "pingTnGov": self.fltrPing(jsonData["pgTnGov"]),
            "procInfo": self.fltrProcInfo(jsonData["topAppMem"]),
            "wireless": self.fltrWireless(jsonData["wireless"]),
            "cpuLoad": self.procCpuLoad(jsonData["cpuLoad"])
            }

        statusDict = self.createStatusDict(diagRecord)
        diagRecord["statusDict"] = statusDict

        self.sendTranToDbs(diagRecord)

    # Get vals from windows KV strings
    def getValRegx(self, strng):

        retrnStr = re.search(r'(:\s+)(.*)', strng)


        return retrnStr.group(2)

    # Get info from info and
    def procSysInfo(self, sysInfoData):

        # Conv strings into array per new line
        sysInfoLines = sysInfoData.splitlines()

        retrnDict = {}

        valsWanted = ['OS Name:', 'OS Version:', 'Total Physical Memory:',
                      'Available Physical Memory:', 'Virtual Memory: Max Size:',
                      'Virtual Memory: Available:', 'Virtual Memory: In Use:']

        # Loop over array with desired info strings
        for val in valsWanted:

            # Loop over lines and if match, add to dict
            for line in sysInfoLines:

                if val in line:
                    lineVal = self.getValRegx(line)
                    retrnDict[val.replace(" ", "")] = lineVal

        return retrnDict

    def procCpuLoad(self, cpuInfoData):

        # Conv strings into array per new line
        retrnDict = {"CpuLoad": re.search(r'[0-9].', cpuInfoData).group(0).rstrip()}

        return retrnDict

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

    def fltrWireless(self, data):

        # Regex

        data = data.splitlines() # Create list from input data

        retrnList = [] # List to be returned from func

        for line in data:

            if not line: continue # If line is empty, continue loop

            # Ignore empty lines
            if re.search(r'[a-z]', line) is None: continue

            # Create list of KV pairs
            lineList = line.split(":")

            # Assign list items to KV pairs
            k = lineList[0].strip()
            v = lineList[1].strip()

            # Ignore interface number line
            if "There is " in k: continue


            # If k has name start a new dict for interface info
            if k == "Name":
                intrfacDict = {}
                intrfacDict[k]=v

            intrfacDict[k]=v

            if "Hosted network status" == k:
                intrfacDict[k]=v
                retrnList.append(intrfacDict)

        return retrnList # Return list


    # Send the transaction to DBs(ES and mongo)
    def sendTranToDbs(self, jsnData):

        mongoTrans = jsnData
        mongoTrans['dateSrvImpt'] = self.dateMongoProc(mongoTrans['dateSrvImpt'])
        self.mDb.addTransac(mongoTrans)


def main():

    ndiag = NetDiag("C:/workspace/TnStateDevops/netTshoot/server")

    print(ndiag.getData())

if __name__ == "__main__":
    main()