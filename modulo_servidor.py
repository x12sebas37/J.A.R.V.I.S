import discord
from jarvis import pensar
prefix = "jarvis"

async def procesar_mensaje_servidor(message):
    texto_usuario = message.content

    if not texto_usuario.startswith(prefix):
        return

    respuesta = pensar(texto_usuario)

    await message.channel.send(respuesta)