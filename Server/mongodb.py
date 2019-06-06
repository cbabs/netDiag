from pymongo import MongoClient
import time
import datetime

class MongoDb(object):
    
    def __init__(self):
        
        dbClient = MongoClient()
        self.db = dbClient['netdiag']
        
        print("Initiate MongoDb success")
        
    
    #Gets records by date
    def getTransDates(self, start, end):
        trans = self.db.tickets.find({'dateUserRan': {'$lt': end, '$gt': start}})
        
        return trans
    
    #Gets a transaction by ticket number
    def getTransTckNum(self, idNum):
        idNum = int(idNum)
        trans = self.db.tickets.find({"ticketNum": idNum})
        
        retrnList = []
        for itms in trans:
            retrnList.append(itms)
        
        for recs in retrnList:
            recs.pop('_id')
        
        return retrnList
    
    # Gets a single transaction by id
    def getTransac(self, idNum):
        idNum = int(idNum)
        trans = self.db.tickets.find_one({"transId": idNum})
        if not trans:
            warning = "No data found in query.  Check trans number "
            return {"ERROR": warning + str(idNum)}
        
        trans.pop("_id")
        return trans
    
    #Gets the last record in a collection
    def getLastRecord(self, collection='netdiag'):
        
        lastTransId = 0 #instaniate var for last id int
        
        #get last record pymongo object
        try:
            colctDict = (self.db.tickets.find().limit(1).sort([("$natural", -1)]))
        except:
            return 0
        
        #Get last id in pymongo object dict and assign to lastTransId
        for rec in colctDict:
            lastTransId = rec['transId']
       
        return lastTransId
        
    #Create a transaction 
    def addTransac(self, jsnData):
        
        lastTransId = self.getLastRecord("tickets")
        nextTransId = lastTransId + 1
        
        #Dict for transaction record 
        jsnData["transId"] = nextTransId
        
        #Add doc to collections
        self.db.tickets.insert_one(jsnData).inserted_id
    
    
    #Return all tickets
    def getAllTrans(self):
        
        retrnList = []
        
        #Get all tickets
        allTrans = self.db.tickets.find({})
        
        #Remove keys needed not needed
        for records in allTrans:
            retrnList.append(records)
        
        return retrnList
    

def main():
    
    mDb = MongoDb()
    
    print(mDb.getTransac(5))
    
    pass
  
if __name__ == '__main__':
    main()
    
    
    
    