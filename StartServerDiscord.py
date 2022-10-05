import discord
import socket
import time
import datetime
import requests
from MCServer import Server, Servers

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in!")
    
    async def handleServerNotFound(self, message, serverName):
        await message.channel.send(f"> Server \"{serverName}\" konnte nicht gefunden werden!")
        time.sleep(5)
        await message.channel.purge(limit=2)

    async def on_message(self, message):
        if (message.author == client.user):
            return
        
        if not message.content.startswith("!server start"):
            return

        serverName = str(message.content).split(" ")[-1]
        ServerInstance = None

        try:
            ServerInstance = Servers[serverName]
        except Exception as e:
            ServerInstance = None

        if not ServerInstance:
            await self.handleServerNotFound(message, serverName)
            return
        
        await ServerInstance.handleRequestToStart(message)

        
client = MyClient()
token = ""
with open("./token.txt", "r") as r:
    token = r.readline()

client.run(token)
