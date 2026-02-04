import discord
from jarvis import pensar
from modulos.modulopedidos import obtener_pedidos
prefix = "jarvis"

async def procesar_mensaje_servidor(message):
    texto_usuario = message.content.lower()

    if not texto_usuario.startswith(prefix):
        return

    comando = texto_usuario.replace(prefix, "").strip()

    if "lista de pedidos" in comando:
        print("Accediendo a la base de datos de Google...")
        pedidos = obtener_pedidos()
        canal_reportes = message.guild.get_channel(1466151763521441867)

        if canal_reportes:
            for pedido in pedidos:
                reporte = f"📦 **Pedido Nuevo**: {pedido['Producto']} - Cliente: {pedido['Nombre']}"
                await canal_reportes.send(reporte)
            return

    respuesta = pensar(texto_usuario)

    await message.channel.send(respuesta)
