import subprocess
import asyncio
import websockets
import json
import ast

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
        print(f"out {msgSend}")

        #TODO Make own func
        msgRecv = await websocket.recv()
        print(f"in {msgRecv}")
        if "remExecCmds" in msgRecv:
            msgDict = ast.literal_eval(msgRecv)
            print(type(msgDict["remExecCmds"]))
            for exeCmd in msgDict["remExecCmds"]:
                cmdReturn = subprocess.run(exeCmd, capture_output=True)
                print(f"out {cmdReturn.stdout.decode()}")
                await websocket.send(cmdReturn.stdout.decode())





asyncio.get_event_loop().run_until_complete(startClient())
asyncio.get_event_loop().run_forever()