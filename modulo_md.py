import discord
from jarvis import pensar, ejecutar_asistente_voz
import threading

async def procesar_mensaje_privado(message):
    texto_usuario = message.content.lower()

    if "activa voz en local" in texto_usuario:
        await message.channel.send("Iniciando voz en local.")

        hilo_voz = threading.Thread(target=ejecutar_asistente_voz)
        hilo_voz.start()

        return

    texto_usuario = message.content
    respuesta = pensar(texto_usuario)
    await message.channel.send(respuesta)