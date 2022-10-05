import socket
import discord
import time
import datetime
import threading
from MCServer import Server, Servers

textkanalid = 851900460867911690
messageid = 922580759108259960

lastMessage = ""
currentMessage = ""

Durchlauf = 0

last = dict.fromkeys(Servers, "offline")


class MyClient(discord.Client):
    def checkServer(self, adress, port) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((adress, port))
        sock.settimeout(None)
        return result

    def getStartedBy(self, fileName) -> str:
        returnvalue = ""
        with open(fileName, "r") as read:
            returnvalue = read.readline()
        return returnvalue

    def getDiscordFormattedText(self, TextArray) -> str:
        value = "> ⠀\n"
        for i in TextArray:
            value += "> "+i + "\n"
        value += "> ⠀\n"
        return value

    def isPCon(self) -> bool:
        socketsheesh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketsheesh.settimeout(5)
        myres = socketsheesh.connect_ex(("192.168.178.42", 3000))
        socketsheesh.settimeout(None)
        return myres == 0

    def getOnlineMessage(self, adresse, started, Servername) -> str:
        returnvalue = self.getDiscordFormattedText(
            [Servername+" ist **online!**", "IP: " + adresse, "gestartet: "+started])
        return returnvalue

    def getOfflineMessage(self, isPCon, Servername) -> str:
        returnvalue = ""
        if (isPCon):
            returnvalue = self.getDiscordFormattedText(
                [Servername + " ist **offline**!", "bereit: **!server start " + str(Servername).lower() + "**"])
        else:
            returnvalue = self.getDiscordFormattedText(
                [Servername+" ist **offline**!"])
        return returnvalue

    async def on_ready(self):
        global last
        global Durchlauf
        global lastMessage
        global currentMessage

        print("Bot is online")
        channel = client.get_channel(textkanalid)
        message = await channel.fetch_message(messageid)
        await client.change_presence(activity=discord.Game("Made by Hendrik und Finn"))

        try:
            while True:
                results = []
                isPCon = self.isPCon()
                currentMessage = ""

                for i in Servers.keys():
                    dataForServer = Servers[i]
                    responseFromCServer = self.checkServer(dataForServer.ip, dataForServer.port)

                    if (responseFromCServer == 0):
                        startedBy = self.getStartedBy(dataForServer.startedByPath)
                        currentMessage += self.getOnlineMessage(dataForServer.joinURL, startedBy, dataForServer.name)
                        last[i] = "online"
                    else:
                        currentMessage += self.getOfflineMessage(
                            isPCon, dataForServer.name)
                        if (last[i] and last[i] != "offline"):
                            with open(dataForServer.startedByPath, "w") as write:
                                write.write("Manuell")
                        last[dataForServer.name] = "offline"

                if "online" in last.values():  # * Wenn der Server läuft
                    if (lastMessage != currentMessage or Durchlauf == 0):
                        await message.edit(content=currentMessage)
                        print("[ " + str(datetime.datetime.now()) +
                              " ] Some Server online [--> Updated]")
                    else:
                        print(
                            "[ " + str(datetime.datetime.now()) + " ] Some Server online")

                else:
                    if (lastMessage != currentMessage or Durchlauf == 0):
                        await message.edit(content=currentMessage)
                        print("[ " + str(datetime.datetime.now()) +
                              " ] Servers offline  [--> Updated]")
                    else:
                        print(
                            "[ " + str(datetime.datetime.now()) + " ] Servers offline")

                lastMessage = currentMessage
                time.sleep(15)
                Durchlauf += 1

        finally:
            await message.edit(content="> \n> Discord-Bot ist **offline!**\n> ⠀")


client = MyClient()
token = ""
with open("./token.txt", "r") as r:
    token = r.readline()
client.run(token)
