from discord.ext import commands
import discord

import flo_games
import config


bot = commands.Bot(command_prefix="!")

@bot.command(name="flogames")
async def flogames(ctx: commands.Context, mmr=2000):
    await ctx.reply(f"Searching for games with mmr above {mmr}")
    games = flo_games.get_flo_games(config.FLO_URL)
    for game in games:
        mmr_flag = False
        embed_content = ""
        for player in game.players:
            if player.mmr >= mmr:
                mmr_flag = True
        
        if mmr_flag == True:
            embed_content += f"**Map**: {game.map}\n"
            embed_content += f"**Start Time**: {game.start_time}\n"
            embed_content += f"**Server**: {game.server}\n\n"
            for player in game.players:
                embed_content += f"[{player.race}] {player.name} - {player.mmr}\n"
            
            embed_content += f"\nGame URL: {game.game_url}"

        if mmr_flag == True:    
            embed = discord.Embed(
                title = f"FloTV Game",
                description = embed_content
            )

            await ctx.reply(embed=embed)
    

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


DISCORD_TOKEN = config.DISCORD_TOKEN
bot.run(DISCORD_TOKEN)
