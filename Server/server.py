import os
import time
import datetime
import json
from pymongo import MongoClient
import subprocess
import jsoncomment
from json.decoder import JSONDecodeError



class NetDiag(object):

    def __init__(self, fileShare, dbHost=None, dbPort=None, dbUser=None, dbPass=None, dbName=None):

        dbClient = MongoClient(dbHost, dbPort,
                               username=dbUser, password=dbPass)
        self.db = dbClient[dbName]
        self.fileShare = fileShare


    # Read files on file share.  If not json, erase.
    def getData(self):
        
        dirLst = os.listdir(self.fileShare) # List of file in dir
        
        # Loop over files in dir
        for file in dirLst:
    
            
    
            # If file ends with .json process
            if file.endswith(".json"):
                
                rmArg = "{}/{}".format(self.fileShare, file)
                
                ## This block removes last line of JSON file.
                ## Needed for JSON lib to read
                
                fRemLast = open(file, "r+", encoding = "utf-8")

                #Move the pointer to the end of the file. 
                fRemLast.seek(0, os.SEEK_END)
                
                # Last char in file
                pos = fRemLast.tell() - 1
                
                #Read each character backwrds until new line
                while pos > 0 and fRemLast.read(1) != "\n":
                    pos -= 1
                    fRemLast.seek(pos, os.SEEK_SET)
                
                # Delete all the chars ahead of this position if ! beginning
                if pos > 0:
                    fRemLast.seek(pos, os.SEEK_SET)
                    fRemLast.truncate()
                
                fRemLast.close() # Close the file
                
                
                # Open file for JSON processing
                with open(file, "r+", encoding='utf-8') as f:

                    fRead = f.read() # Read file into string

                    # Keep line breaks in json wrapper(see jsonComment docs)
                    fRead2 = fRead.replace("\n","\n\\n")

                    json = JsonComment() # Call JSON wrapper                    
                    jsonData = json.loads(fRead2) # Convert to JSON

                    dbData = self.processData(jsonData)
                    
                    f.close()
                    
                    

                    
                print(rmArg)
                #subprocess.run(["rm", rmArg]) # Remove the file
            
    
            #self.processData(jsonData) # Process raw JSON data
    
    def processData(self, jsonData):
        print(jsonData)
        
        transDict = None

        tStamps = self.getTimeStamps()

        ip = jsonData["ip"]
        print(type(ip))

        # Dict for transaction record
        diagRecord = {
            "dateSrvImpt": tStamps["timeStmp"],
            "epochSrvImpt": tStamps["epoch"],
            "dateUserRan": jsonData["runTmStmp"].replace("\n", ""),
            "userId": jsonData["userId"].replace("\n", ""),
            "ticketNum": jsonData["ticketNum"].replace("\n", ""),
            "ipconfig": self.fltrIpInfo(ip),
            "traceGoglDns": self.fltrTracRt(jsonData["trcRtPubDns"]),
            "traceSdcDns": self.fltrTracRt(jsonData["trcRtSdcDns"]),
            "traceNdcDns": self.fltrTracRt(jsonData["trcRtNdcDns"]),
            "traceTnGov": self.fltrTracRt(jsonData["trcRtTnGov"]),
            "pingGoglDns": self.fltrPing(jsonData["pgPubDns"]),
            "pingSdcDns": self.fltrPing(jsonData["pgSdcDns"]),
            "pingNdclDns": self.fltrPing(jsonData["pgNdcDns"]),
            "pingTnGov": self.fltrPing(jsonData["pgTnGov"])
            }
        
        self.addTransac(diagRecord)

    # Create a transaction
    def addTransac(self, transDict):
        
        print(transDict)
        return
        
        # I should put a comment here
        lastTransId = self.getLastRecord("transactions")
        nextTransId = lastTransId + 1

        # Add doc to collections
        record = self.db.transactions.insert_one(transDict).inserted_id
        
        
        return record["transId"]

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
            
            print(line)
            
            if not line: continue # If line is empty, continue loop
            
            # Ignore lines with Trace complete and empty ones
            if "Trace complete" in line: continue
            if re.search(r'[a-z]', line) is None: continue
            
            wrdsLst = re.findall(regxWords, line) # List from words in line
            digtLst = re.findall(regxDigts, line) # List from words in line

            
            if "Tracing" in line:
                ipAddr = re.search(regxIpAddr, line)
                print(ipAddr[0])
                retrnDict["ipAddr"] = ipAddr[0]
                continue
            
               
            if "over a" in line: continue
    
            # Dict to append to list
            lineDict = {
                "tracOrdrNum": digtLst[0],
                "trip1time": digtLst[1],
                "trip2time": digtLst[2],
                "trip3time": digtLst[3],
                "ipHop": digtLst[4]
                }       
        
            retrnDict["traceList"].append(lineDict) # Append list to be returned
                
        return retrnDict
    
    
    # Process process info into list of dicts
    def fltrProcInfo(self, data):
    
        # Regex
        regxWords = '[a-zA-Z0-9_\.,]+'
    
        data = data["topAppMem"].splitlines() # Create list from input data
    
        retrnLst = [] # List to be returned from func
        
        for line in data:
            
            # Only check lines with 'K' at end
            if re.search(r'K$', line):
    
                wrdsLst = re.findall(regxWords, line) # List from words in line
            
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
                
                print(lineDict)
                
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
                retrnDict["latncyMin"] = lineWords[0]
                retrnDict["latncyMax"] = lineWords[1]
                retrnDict["latncyAvg"] = lineWords[2]
                continue      
                
        return retrnDict # Return dict


def main():
    
    pass

if __name__ == "__main__":
    main()