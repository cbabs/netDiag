import subprocess
import asyncio
import websockets
import json
import ast

#TODO remove this import after testing done
import random

def runOsCmd(osCmd):

    retrnData = subprocess.run(osCmd, capture_output=True)
    #retrnData = retrnData.stdout.decode('UTF-8')
    retrnData = retrnData.stdout
    #retrnData = retrnData.replace('\r\n', '\n')

    return retrnData


async def startClient():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        hostName = runOsCmd("hostname")
        hostName = hostName.decode('UTF-8').strip().replace('\r\n', '\n') + "+" + str(random.randint(1, 50))
        print(hostName)

        msgSend = {"regstrMchine": hostName}
        msgSend = json.dumps(msgSend)

        await websocket.send(msgSend)      

        #TODO Make own func
        async for message in websocket:
            
            print("handler loop " + str(message))
            print(message)
            msgRecv = message
            print(f"in  {msgRecv}")
            #   await processWsMesg(msgRecv, websocket, hostName)


#async def processWsMesg(msgRecv, websocket, hostName):
            if "run_report" in msgRecv:    
                try:
                    print(subprocess.run("client", capture_output=True))
                except Exception as e:
                    print('ERROR')
                    print(e)
                    await websocket.send(str(e))
                continue


            if "remExecCmds" in msgRecv:
                print(msgRecv)
                msgDict = ast.literal_eval(msgRecv)
                print(type(msgDict["remExecCmds"]))
                for exeCmd in msgDict["remExecCmds"]:
                    exeCmd = exeCmd.split(" ")
                    cmdReturn = None
                    try:
                        cmdReturn = subprocess.run(exeCmd, capture_output=True, timeout=20)
                        cmdReturn = cmdReturn.stdout
                    except Exception as e:
                        print(e)
                        cmdReturn = e
                    
                    msgToSend = f'{{"{hostName}":{cmdReturn}}}'
                    print(f"out > {msgToSend}")
                    await websocket.send(msgToSend)
            




def main():
    asyncio.get_event_loop().run_until_complete(startClient())
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()