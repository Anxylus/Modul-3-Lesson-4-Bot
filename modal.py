import discord
from discord.ext import commands
from discord import ui, TextStyle, ButtonStyle

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class AdminModal(ui.Modal, title="Admin Panel"):
    nickname = ui.TextInput(label="Nickname baru", required=False)
    channel_name = ui.TextInput(label="Nama channel baru", required=False)
    ban_reason = ui.TextInput(label="Alasan ban", style=TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild

        # Permission check
        if not member.guild_permissions.administrator:
            return await interaction.response.send_message(
                "❌ Kamu bukan admin.", ephemeral=True
            )

        # Rename
        if self.nickname.value:
            await member.edit(nick=self.nickname.value)

        # Create channel
        if self.channel_name.value:
            await guild.create_text_channel(self.channel_name.value)

        # Ban
        if self.ban_reason.value:
            await guild.ban(member, reason=self.ban_reason.value)

        await interaction.response.send_message(
            "✅ Aksi admin berhasil dijalankan.", ephemeral=True
        )


class AdminButton(ui.Button):
    def __init__(self):
        super().__init__(
            label="Admin Panel",
            style=ButtonStyle.danger
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AdminModal())


class AdminView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AdminButton())


@bot.command()
async def admin(ctx):
    await ctx.send("🔧 Panel Admin:", view=AdminView())


@bot.event
async def on_ready():
    print(f"Login sebagai {bot.user}")

bot.run("wuahahah :v")