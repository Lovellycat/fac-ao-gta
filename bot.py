import discord
import os
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ADMIN_ROLE_ID = 123456789012345678  # ⚠️ ALTERE PARA O ID DO CARGO DE ADMIN

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    button = Button(label="Criar meu chat privado", style=discord.ButtonStyle.green, custom_id="create_private_channel")

    async def button_callback(interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        existing_channel = discord.utils.get(guild.text_channels, name=f"privado-{member.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"❌ Você já tem um canal: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True),
            guild.get_role(1418590512314843250): discord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(
            name=f"privado-{member.name}",
            overwrites=overwrites
        )

        await interaction.response.send_message(f"✅ Canal criado: {channel.mention}", ephemeral=True)
        await channel.send(f"Olá, {member.mention}! Chat privado da facção.")

    button.callback = button_callback
    view = View(timeout=None)
    view.add_item(button)
    await ctx.send("👇 Clique para criar seu chat privado:", view=view)

import os
bot.run(os.getenv(1418590512314843250))
