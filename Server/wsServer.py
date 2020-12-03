import asyncio
import websockets
import json
from aioconsole import ainput
import aio_pika
import ast


import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class wsServer(object):

    def __init__(self, portNum=8765):

        self.portNum = portNum
        self.connected = {}
        self.STATE = {"value": 0}
        self.USERS_MAPPING = []

        self.start_server = websockets.serve(self.srvHandler, '',
                                             portNum, compression=None)

        self.lock = asyncio.Lock()

        self.queue_receive = "recv_cmds_queue"
        self.queue_reply_cmds = "reply_cmds_queue"
        
        asyncio.ensure_future(self.start_rabbit_consumer())
        
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


    async def register(self, hostname, websocket):
        self.USERS_MAPPING.append([hostname, websocket])


    async def unregister(self, websocket):

        # Lock list to prevent race condition
        async with self.lock: 
            userMappingListCopy = self.USERS_MAPPING

            for inx, val in enumerate(userMappingListCopy):

                if val[1] == websocket:
                    self.USERS_MAPPING.pop(inx)


    async def processClientHostname(self, recvData):
        msgRecv = json.loads(recvData)
        hostname = msgRecv["regstrMchine"].replace("\n", "")
        return hostname.strip()


    async def getWsObjectByHostname(self, hostname):
        for item in self.USERS_MAPPING:
            if item[0] == hostname:
                return item[1]


    async def sendCmdsToClient(self, hostname, cmdsToExecute):
        websocket = await self.getWsObjectByHostname(hostname)
        print(cmdsToExecute)
        strOfCmds = f'{{"remExecCmds": ["{cmdsToExecute}"]}}'

        await websocket.send(strOfCmds)


    async def registerClient(self, websocket):
        msgRecv = await websocket.recv() # Get hostname sent from client
        clntHostname = await self.processClientHostname(msgRecv)

        await self.register(clntHostname, websocket)


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
            routing_key = self.queue_receive

            channel = await connection.channel()

            # Declaring queue
            queue = await channel.declare_queue(self.queue_reply_cmds,
                                                auto_delete=True)

            await channel.default_exchange.publish(
            aio_pika.Message(body=sendingMsg.encode(), expiration=30),
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
        queue = await channel.declare_queue(self.queue_receive,
                                            auto_delete=True)

        # Send message to func
        await queue.consume(self.process_rabbit_message)


    async def srvHandler(self, websocket, path):
        await self.registerClient(websocket)

        try:
            async for message in websocket:

                await self.send_rabbit_message(message,
                self.queue_reply_cmds)
                
        finally:
            await self.unregister(websocket)


def main():

    wss = wsServer()
    wss()

if __name__ == "__main__":
    main()