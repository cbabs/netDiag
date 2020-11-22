import asyncio
import websockets
import json
from aioconsole import ainput


import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class wsServer(object):

    def __init__(self, portNum=8765):

        self.portNum = portNum

        print("weServer class instantiating")

        self.connected = {}
        self.STATE = {"value": 0}
        self.USERS = set()
        self.USERS_MAPPING = []

        self.start_server = websockets.serve(self.srvHandler, 'localhost', portNum)

        asyncio.ensure_future(self.console_input())
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()



    async def register(self, hostname, websocket):
        self.USERS.add(websocket)
        self.USERS_MAPPING.append([hostname, websocket])


    async def unregister(self, websocket):
        self.USERS.remove(websocket)

        
        userMappingListCopy = self.USERS_MAPPING

        for inx, val in enumerate(userMappingListCopy):

            if val[1] == websocket:
                self.USERS_MAPPING.pop(inx)



    async def processClientHostname(self, recvData):

        print(recvData)
        print(type(recvData))
        msgRecv = json.loads(recvData)
        hostname = msgRecv["regstrMchine"].replace("\n", "")
        return hostname.strip()

    async def getWsObjectByHostname(self, hostname):
        for item in self.USERS_MAPPING:
            if item[0] == hostname:
                return item[1]



    async def sendAndGetCmds(self, hostname, cmdsToExecute):
        websocket = await self.getWsObjectByHostname(hostname)

        if "," in cmdsToExecute:
            cmdList = cmdsToExecute.split(',')
        else:
            cmdList = [cmdsToExecute]

        print(cmdList)
        strOfCmds = f'{{"remExecCmds": {cmdList}}}'
        print(strOfCmds)
        await websocket.send(strOfCmds)
        cmdRecv = await websocket.recv()
        print(cmdRecv)


    async def console_input(self):
        hostname = await ainput('Enter hostname: ')
        exeCmd = await ainput('Enter cmd: ')
        await self.sendAndGetCmds(hostname, exeCmd)

    async def consumer_handler(websocket, path):
        async for message in websocket:
            await consumer(message)
            
            
    async def producer_handler(websocket, path):
        while True:
            message = await producer()
            await websocket.send(message)


    async def srvHandler(self, websocket, path):
        # register(websocket) sends user_event() to websocket


        msgRecv = await websocket.recv() # Get hostname sent from client
        clntHostname = await self.processClientHostname(msgRecv)

        await self.register(clntHostname, websocket)
        print(self.USERS_MAPPING)


        try:
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "minus":
                    STATE["value"] -= 1
                    await notify_state()
                elif data["action"] == "plus":
                    STATE["value"] += 1
                    await notify_state()
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)



'''     ##Code prior to client registration

    async def srvHandlr(self, websocket, path):

        # Registration
        print("running srvHandlr func from class init")

        msgRecv = await websocket.recv()
        msgRecv = json.loads(msgRecv)


        hostname = msgRecv["regstrMchine"].replace("\n", "")
        hostname = hostname.strip()


        self.connected[hostname] = websocket

        print(self.connected)

        greeting = f"Hello {self.connected}!"

        #await websocket.send(greeting)
        print(f"> {greeting}")
        await websocket.send('{"remExecCmds": ["ipconfig", "ping 8.8.8.8"]}')
        cmdRecv = await websocket.recv()
        print(cmdRecv)



    def sendCmd(self, hostname, command):
        num = 1
        while num < 5:
            print("Printing")
            print(num)
            print(self.connected)
            time.sleep(5000)
            num += 1
    '''


def main():

    wss = wsServer()



    wss()

    wss.sendCmd("DESKTOP-RGFH0PI", "whoami")


if __name__ == "__main__":
    main()