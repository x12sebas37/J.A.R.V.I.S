import discord
import os
from dotenv import load_dotenv
from jarvis import pensar
import modulo_md
import modulo_servidor

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Sistemas de discord en linea. Sesion iniciada en: {client.user}")
    modulo_servidor.iniciar_vigilancia(client)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.guild is None:

        await modulo_md.procesar_mensaje_privado(message)

    else: 

        await modulo_servidor.procesar_mensaje_servidor(message)

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
