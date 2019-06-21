import subprocess
import asyncio
import websockets
import json

def runOsCmd(osCmd):

    retrnData = subprocess.run(osCmd, capture_output=True)
    retrnData = retrnData.stdout.decode('UTF-8')
    retrnData = retrnData.replace('\r\n', '\n')

    return retrnData


async def startClient():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        hostName = runOsCmd("hostname")

        msgSend = {"regstrMchine": hostName}
        msgSend = json.dumps(msgSend)

        print(type(msgSend))
        #print(type(msgSend["regstrMchine"]))


        await websocket.send(msgSend)
        print(f"> {msgSend}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(startClient())
asyncio.get_event_loop().run_forever()