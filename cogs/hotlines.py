import discord
from discord import app_commands
from discord.ext import commands

class HotlinesCog(commands.Cog):
    # Country name to ISO code mapping for dynamic flag generation
    COUNTRY_TO_ISO = {
        "United States": "US", "Canada": "CA", "United Kingdom": "GB",
        "Australia": "AU", "France": "FR", "Germany": "DE", "Belgium": "BE",
        "Spain": "ES", "Italy": "IT", "Japan": "JP", "India": "IN",
        "Brazil": "BR", "Mexico": "MX", "South Africa": "ZA", "New Zealand": "NZ",
        "Netherlands": "NL", "Sweden": "SE", "Switzerland": "CH", "South Korea": "KR",
        "China": "CN", "Argentina": "AR", "Portugal": "PT", "Poland": "PL",
        "Norway": "NO", "Finland": "FI", "Philippines": "PH", "Turkey": "TR",
        "Russia": "RU", "Greece": "GR", "Israel": "IL", "Malaysia": "MY",
        "Singapore": "SG", "Thailand": "TH", "Ukraine": "UA", "Egypt": "EG",
        "Ireland": "IE", "Denmark": "DK"
    }

    def get_flag(self, country_name: str) -> str:
        """Dynamically generate flag emoji from country name"""
        iso = self.COUNTRY_TO_ISO.get(country_name)
        if iso:
            # Convert ISO code to flag emoji (regional indicator symbols)
            return ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in iso.upper())
        return "🌍"  # Default globe

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

        flag = self.get_flag(country_key)
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
        # Dynamic flags in list
        country_list = [f"{self.get_flag(c)} {c}" for c in sorted(countries)]
        msg = "**Available Countries:**\n• " + "\n• ".join(country_list)
        await interaction.followup.send(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HotlinesCog(bot))
    print("✅ Hotlines cog loaded with dynamic flags")