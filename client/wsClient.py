import subprocess
import asyncio
import websockets
import json
import ast
import time


def runOsCmd(osCmd):

    retrnData = subprocess.run(osCmd, capture_output=True)
    retrnData = retrnData.stdout

    return retrnData

async def wsHandler():
    while True:
        try:
            await startClient()
        except:
            print("Connection failed. Will try again in 60 secs")
            time.sleep(60)
        else:
            break


async def startClient():
    async with websockets.connect(
            f'ws://10.100.0.113:8765') as websocket:
        print("Connected to server!")
        hostName = runOsCmd("hostname")
        hostName = hostName.decode('UTF-8').strip().replace('\r\n', '\n')
        print(hostName)

        msgSend = {"regstrMchine": hostName}
        msgSend = json.dumps(msgSend)

        await websocket.send(msgSend)

        async for message in websocket:

            print("handler loop " + str(message))
            print(message)
            msgRecv = message
            print(f"in < {msgRecv}")

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
    print(__name__)
    asyncio.get_event_loop().run_until_complete(wsHandler())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()