import discord
from discord import app_commands
from discord.ext import commands

class HotlinesCog(commands.Cog):
    FLAGS = {
        "United States": "🇺🇸", "Canada": "🇨🇦", "United Kingdom": "🇬🇧",
        "Australia": "🇦🇺", "France": "🇫🇷", "Germany": "🇩🇪", "Belgium": "🇧🇪",
        "Spain": "🇪🇸", "Italy": "🇮🇹", "Japan": "🇯🇵", "India": "🇮🇳",
        "Brazil": "🇧🇷", "Mexico": "🇲🇽", "South Africa": "🇿🇦", "New Zealand": "🇳🇿",
        "Netherlands": "🇳🇱", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "South Korea": "🇰🇷",
        "China": "🇨🇳", "Argentina": "🇦🇷", "Portugal": "🇵🇹", "Poland": "🇵🇱",
        "Norway": "🇳🇴", "Finland": "🇫🇮", "Philippines": "🇵🇭", "Turkey": "🇹🇷",
        "Russia": "🇷🇺", "Greece": "🇬🇷", "Israel": "🇮🇱", "Malaysia": "🇲🇾",
        "Singapore": "🇸🇬", "Thailand": "🇹🇭", "Ukraine": "🇺🇦", "Egypt": "🇪🇬",
        "Ireland": "🇮🇪", "Denmark": "🇩🇰"
    }

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all mental health commands")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title="🆘 Mental Health Help Center", color=0x00b4d8)
        embed.description = "You are not alone. Help is available 24/7."
        embed.add_field(name="📋 Commands", value="`/help` - Show this menu\n`/hotline` - Get hotlines\n`/list_countries` - See all countries\n`/crisis` - Immediate crisis support", inline=False)
        embed.set_footer(text="All messages are private • Take care of yourself")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="crisis", description="Immediate crisis support")
    async def crisis(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title="🚨 Crisis Support", color=0xff4444)
        embed.description = "If you're in immediate danger or crisis, reach out right now."
        embed.add_field(name="🇺🇸 United States", value="**988** - Suicide & Crisis Lifeline (24/7)", inline=False)
        embed.add_field(name="🇨🇦 Canada", value="**1-833-456-4566** - Talk Suicide Canada", inline=False)
        embed.add_field(name="🌍 More Options", value="Use `/hotline` or visit [findahelpline.com](https://findahelpline.com)", inline=False)
        embed.set_footer(text="You matter. Help is here.")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="hotline", description="Find mental health hotlines")
    @app_commands.describe(country="Country name", state="State or Province (optional)")
    async def hotline(self, interaction: discord.Interaction, country: str, state: str = None):
        await interaction.response.defer(ephemeral=True)
        
        data = getattr(self.bot, 'hotlines_data', {}).get("countries", {})
        search = country.lower().strip()
        
        country_key = None
        for key in data.keys():
            if search in key.lower() or key.lower() in search:
                country_key = key
                break
        
        if not country_key:
            await interaction.followup.send(f"❌ Could not find **{country}**.\nTry `/list_countries`", ephemeral=True)
            return

        flag = self.FLAGS.get(country_key, "🌍")
        embed = discord.Embed(title=f"{flag} {country_key} Hotlines", color=0x00ff88)
        
        for h in data[country_key].get("national", []):
            embed.add_field(name=h.get("name"), value=f"**{h.get('number')}**\n{h.get('notes','')}", inline=False)
        
        if state:
            regions = data[country_key].get("states") or data[country_key].get("provinces", {})
            if state in regions:
                for h in regions[state]:
                    embed.add_field(name=f"📍 {state} - {h.get('name')}", value=f"**{h.get('number')}**\n{h.get('notes','')}", inline=False)
        
        embed.set_footer(text="Private message • Always verify the number • You are not alone")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="list_countries", description="List all available countries")
    async def list_countries(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        countries = list(getattr(self.bot, 'hotlines_data', {}).get("countries", {}).keys())
        msg = "**Available Countries:**\n• " + "\n• ".join(sorted(countries))
        await interaction.followup.send(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HotlinesCog(bot))
    print("✅ Hotlines cog loaded with flags")