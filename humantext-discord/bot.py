import discord
from discord import app_commands
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URL = os.getenv('API_URL', 'http://localhost:8000/api/v1')

class HumanTextBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Bot is ready and slash commands are synced.")

client = HumanTextBot()

@client.tree.command(name="humanize", description="Make AI text undetectable using LangGraph agents.")
@app_commands.describe(
    text="The AI text you want to humanize",
    strength="Rewrite intensity (light, medium, aggressive)"
)
@app_commands.choices(strength=[
    app_commands.Choice(name="Ninja (Light)", value="light"),
    app_commands.Choice(name="Balanced (Medium)", value="medium"),
    app_commands.Choice(name="Ghost (Aggressive)", value="aggressive")
])
async def humanize(interaction: discord.Interaction, text: str, strength: app_commands.Choice[str] = None):
    await interaction.response.defer(thinking=True)
    
    rewrite_strength = strength.value if strength else "medium"
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. Trigger the job
            post_data = {"text": text, "strength": rewrite_strength}
            async with session.post(f"{API_URL}/humanize/advanced", json=post_data) as response:
                if response.status != 200:
                    await interaction.followup.send("❌ Error: Could not reach HumanText API.")
                    return
                data = await response.json()
                job_id = data.get("job_id")
                
            if not job_id:
                await interaction.followup.send("❌ Error: No Job ID returned.")
                return

            # 2. Poll for completion
            max_retries = 30
            for i in range(max_retries):
                async with session.get(f"{API_URL}/jobs/{job_id}") as poll_res:
                    poll_data = await poll_res.json()
                    status = poll_data.get("status")
                    
                    if status == "completed":
                        best_output = poll_data["result"]["candidates"][0] if poll_data["result"].get("candidates") else poll_data["result"].get("final_output", "No output")
                        
                        embed = discord.Embed(title="✨ HumanText Complete", color=0x3b82f6)
                        embed.add_field(name="Original", value=text[:1000], inline=False)
                        embed.add_field(name=f"Humanized ({rewrite_strength.title()} Mode)", value=best_output[:1000], inline=False)
                        embed.set_footer(text="Powered by LangGraph & Qwen2.5")
                        
                        await interaction.followup.send(embed=embed)
                        return
                    elif status == "failed":
                        await interaction.followup.send("❌ Error: Humanization failed on backend.")
                        return
                        
                await asyncio.sleep(2)
                
            await interaction.followup.send("⏳ Timeout: Agents took too long to respond.")
            
        except Exception as e:
            await interaction.followup.send(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
    else:
        client.run(TOKEN)
