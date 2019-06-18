import asyncio
import websockets
import json


class wsServer(object):

    def __init__(self, portNum=8765):

        self.portNum = portNum

        print("Class instantiating")

        connected = set()


        async def srvHandlr(websocket, path):

            # Registration
            connected.add(websocket)

            msgRecv = await websocket.recv()
            msgRecv = json.loads(msgRecv)




            print(type(msgRecv))



            greeting = f"Hello {msgRecv}!"

            await websocket.send(greeting)
            print(f"> {greeting}")

        start_server = websockets.serve(srvHandlr('localhost', 8765)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

def main():

    wss = wsServer()

    wss()


if __name__ == "__main__":
    main()