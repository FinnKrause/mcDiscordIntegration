import datetime
import socket
import time
import requests

class Server():
    def __init__(self, ip, port, testLink, startLink, startedByPath, name, joinURL):
        self.ip = ip
        self.port = port
        self.testLink = testLink
        self.startLink = startLink
        self.startedByPath = startedByPath
        self.name = name
        self.joinURL = joinURL

    def isOnline(self, message):
        print("[" + str(datetime.datetime.now()) +
              f"] Prüfung --> {message.author}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((self.ip, self.port))
        sock.settimeout(None)
        return result

    async def startServer(self, message):
        r = requests.post(self.startLink, data={}, timeout=5)
        if r.status_code == 200:
            await message.channel.send("> Server startet!")
            print("[" + str(datetime.datetime.now()) +
                  f"] Server gestartet von --> {message.author}")
            with open(self.startedByPath, "w") as write:
                write.write(str(message.author))
            time.sleep(20)
            await message.channel.purge(limit=3)
            print("[" + str(datetime.datetime.now()) +
                  f"] Nachrichten gelöscht! --> {message.author}")
            return r

    async def handleStartError(self, message, e):
        await message.channel.send("> Finns's PC ist aus oder es gab einen anderen Fehler!")
        print(f"[" + str(datetime.datetime.now()) +
              f"] Anfrage von --> {message.author} FEHLER({str(e)})")
        time.sleep(20)
        await message.channel.purge(limit=3)
        print("[" + str(datetime.datetime.now()) +
              f"] Nachrichten gelöscht! --> {message.author}")

    async def handleAlreadyOn(self, message):
        await message.channel.send("> Server läuft schon!")
        print("[" + str(datetime.datetime.now()) +
              f"] Server läuft schon! --> {message.author}")
        time.sleep(20)
        await message.channel.purge(limit=3)
        print("[" + str(datetime.datetime.now()) +
              f"] Nachrichten gelöscht! --> {message.author}")

    async def handleRequestToStart(self, message):
        await message.channel.send("> Prüfung...")

        result = self.isOnline(message)

        if result == 0:
            await self.handleAlreadyOn(message)

        else:
            try:
                await self.startServer(message)
            except Exception as e:
                await self.handleStartError(message, e)
        print("")


Servers = {
    "mainserver": Server('192.168.178.42', 25565, "http://192.168.178.42:3000/test", "http://192.168.178.42:3000/on", "./ServerStarts/MainServerStarted.txt", "Mainserver", "mc.finnkrause.com"),
    "hiddenserver": Server('192.168.178.42', 25566, "http://192.168.178.42:2999/test", "http://192.168.178.42:2999/on", "./ServerStarts/NewServerStarted.txt", "Hiddenserver", "hiddenserver.finnkrause.com"),
    "modserver": Server('192.168.178.42', 25567, "http://192.168.178.42:2998/test", "http://192.168.178.42:2998/on", "./ServerStarts/ModServerStarted.txt", "Modserver", "mmc.finnkrause.com"),
}