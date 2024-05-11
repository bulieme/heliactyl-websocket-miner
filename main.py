import asyncio
import json
import websockets
import time, math

#its not effective


async def websocket():
    s = 0
    async for websocket in websockets.connect(url, extra_headers={"Cookie":cookie}):
        try:
            while True:
                secondsInSession = s % 60
                minutesInSession = math.floor(s / 60) % 3600
                hoursInSession = math.floor(s / 3600)
                send = await websocket.send(json.JSONEncoder().encode({"type":"ping"}))
                print("<<< "+json.JSONEncoder().encode({"type":"ping"}))
                sessionDuration = ""
                if hoursInSession < 0:
                    sessionDuration += f"{hoursInSession} hours, {minutesInSession} minute, {secondsInSession} seconds"
                if (minutesInSession > 0) or (hoursInSession > 0):
                    sessionDuration += f"{minutesInSession} minute, {secondsInSession} seconds"
                else:
                    sessionDuration += f"{secondsInSession} seconds"
                print(sessionDuration)
                time.sleep(1)
                s += 1
            recieved = await websocket.recv()
            print(f">>> {recieved}")
        except websockets.ConnectionClosed:
            s = 0
            continue

while True:
    url = input("WebSocket Url >>> ")
    if not (("ws://" in url) or ("wss://" in url)):
        input(f"INVALID URL: {url}\n\nPress Enter to try again...")
    else:
        break

cookie = input("Cookie >>> ")

if __name__ == "__main__":
    try:
        asyncio.run(websocket())
    except KeyboardInterrupt:
        print("exit")
