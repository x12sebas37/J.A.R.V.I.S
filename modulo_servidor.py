import discord
from jarvis import pensar
from modulos.modulopedidos import obtener_pedidos
from discord.ext import tasks
prefix = "jarvis"
total_pedidos_vistos = 0

class PanelPedidos(discord.ui.View):
    def __init__(self, pedido_especifico):
        super().__init__(timeout=None)
        self.pedido = pedido_especifico

    @discord.ui.button(label="✅ Hecho", style=discord.ButtonStyle.green)
    async def confirmar_pedido(self, interaction: discord.Interaction, button: discord.ui.Button):
        ID_DESTINO = 1469204780906844213
        canal = interaction.client.get_channel(ID_DESTINO)

        if canal:
            confirmacion = (
                f"Hola {self.pedido['Nombre']} puedes confirmarnos si los siguiendes datos son correctos:\n"
                f"Ciudad: {self.pedido['Ciudad']}\n"
                f"Departamento: {self.pedido['Departamento']}\n"
                f"Direccion: {self.pedido['Direccion']}\n"
                f"Numero: {self.pedido['Numero']}\n"
                f"Talla: {self.pedido['Talla']}\n"
                f"Producto: {self.pedido['Producto']}\n" 
                "Por favor confirmanos si los datos son correctos"
            )

            await canal.send(confirmacion)

            await interaction.response.send_message("Pedido enviado al canal de logística, señor.", ephemeral=True)

def iniciar_vigilancia(client_principal):
    global client
    client = client_principal # Ahora el módulo ya conoce al transmisor
    auto_pedido.start()

@tasks.loop(seconds=30)
async def auto_pedido():
    global total_pedidos_vistos

    pedidos_actuales = obtener_pedidos()
    conteo_ahora = len(pedidos_actuales)

    # Todo lo que sigue debe estar DENTRO de este primer IF
    if conteo_ahora > total_pedidos_vistos: 

        if total_pedidos_vistos == 0: 
            total_pedidos_vistos = conteo_ahora
            return
            
        # Observe el espacio extra a la izquierda de estas líneas:
        print("Nuevo pedido detectado")
        ultimo_pedido = pedidos_actuales[-1]

        canal_reportes = client.get_channel(1466151763521441867)

        if canal_reportes:
            vista = PanelPedidos(pedido_especifico=ultimo_pedido)
            embed = discord.Embed(title="🚀 Nuevo pedido registrado", color=0x2A108F)
            embed.add_field(name="Producto:", value=ultimo_pedido["Producto"])
            embed.add_field(name="Nombre:", value=ultimo_pedido["Nombre"])
            embed.add_field(name="Dirección:", value=ultimo_pedido["Direccion"])
            embed.add_field(name="Ciudad:", value=ultimo_pedido["Ciudad"])
            embed.add_field(name="Departamento:", value=ultimo_pedido["Departamento"])
            embed.add_field(name="Número:", value=ultimo_pedido["Numero"])
            embed.add_field(name="Talla:", value=ultimo_pedido["Talla"])

            await canal_reportes.send(embed=embed, view=vista)

        # Actualizamos la memoria solo cuando terminamos de avisar
        total_pedidos_vistos = conteo_ahora


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
