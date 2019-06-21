import asyncio
import websockets
import json


import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class wsServer(object):

    def __init__(self, portNum=8765):

        self.portNum = portNum

        print("Class instantiating")

        self.connected = {}


        async def srvHandlr(websocket, path):

            # Registration
            

            msgRecv = await websocket.recv()
            msgRecv = json.loads(msgRecv)
            
            
            hostname = msgRecv["regstrMchine"].replace("\n", "")
            hostname = hostname.strip()
            
            
            self.connected[hostname] = websocket
            
            print(self.connected)

            greeting = f"Hello {self.connected}!"

            await websocket.send(greeting)
            print(f"> {greeting}")

        start_server = websockets.serve(srvHandlr, 'localhost', 8765)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        
    def sendCmd(self, hostname, command):
        num = 1
        while num < 5:
            print("Printing")
            print(num)
            print(self.connected)
            time.sleep(5000)
            num += 1
        
        

def main():

    wss = wsServer()
    
    

    wss()
    
    wss.sendCmd("DESKTOP-RGFH0PI", "whoami")


if __name__ == "__main__":
    main()