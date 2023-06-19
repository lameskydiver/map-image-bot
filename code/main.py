import discord
from discord import app_commands
import serverstats
import mapimg
import formatting
import numpy as np

"""
Map score is heavily dependent on the average playercount, and the total duration of the map played
Score = sigma_s(ession) (player_s/server cap_s) * duration_s
"""

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guild_id = 0        #your guild id here
dev_channel_id = 0  #id of a channel within your guild that is not used for map tracking

#Bot command to record map tracking data from a given date and time input
@tree.command(name = "record", description = "Records maps played from a certain date and time", guild=discord.Object(id=guild_id))
@app_commands.describe(timestamp_start="The starting date and time in form at of YYYY-MM-DD HH:MM (set at UTC+0)")
@app_commands.describe(timestamp_end="The ending date and time in form at of YYYY-MM-DD HH:MM (set at UTC+0)")
@app_commands.describe(csv_name="Name of the server to search for")
async def record(interaction, timestamp_start: str, timestamp_end: str, csv_name: str=None):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#1061776942631751701> channel!')
        return
    await interaction.response.send_message("Working to record map tracks from ***"+timestamp_start+"*** to ***"+timestamp_end+"***...")
    if(csv_name==None):
        for channel in interaction.channel.category.channels:
            if(channel.name == 'dev'): continue
            await mapimg.recordMapTrackEmbed(interaction, channel, timestamp_start, timestamp_end)
    else:
        channel = None
        for channels in interaction.channel.category.channels:
            if(channels.name == csv_name):
                channel = channels
                break
        await mapimg.recordMapTrackEmbed(interaction, channel, timestamp_start, timestamp_end)

#Bot command to find map tracks with missing images
@tree.command(name = "findinvalidmapimg", description = "With a given .csv name finds maps that do not have a valid map image", guild=discord.Object(id=guild_id))
@app_commands.describe(csv_name="Name of the server to search for")
async def findinvalidmapimg(interaction, csv_name: str=None):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    data = []
    if(csv_name==None):
        await interaction.response.send_message("Working to find maps with a missing image for all tracked servers...")
        for channel in interaction.channel.category.channels:
            if(channel.name == 'dev'): continue
            data = mapimg.consolidateInvalidMapImg(data,channel.name)
        await mapimg.analyseMapImg(interaction, data, 'list')
        await interaction.edit_original_response(content="Succesfully found all maps with a missing image for all tracked servers.")
    else:
        await interaction.response.send_message("Working to produce maps with a missing image for "+csv_name+"...")
        data = mapimg.consolidateInvalidMapImg(data,csv_name)
        await mapimg.analyseMapImg(interaction, data, csv_name)
        await interaction.edit_original_response(content="Succesfully found all maps with a missing image for "+csv_name+".")

#Bot command to display stats of a server
@tree.command(name = "statsserver", description = "Display map statistics of a given server", guild=discord.Object(id=guild_id))
@app_commands.describe(server_name="Name of server to get statistics for")
async def statsserver(interaction, server_name: str):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await interaction.response.send_message("Displaying statistics of "+server_name+"...")
    await serverstats.calculateServerStat(interaction, server_name)

#Bot command to reorganise serverstats csv by longest duration
@tree.command(name = "statsserverduration", description = "Display map statistics of a given server by the longest played duration", guild=discord.Object(id=guild_id))
@app_commands.describe(server_name="Name of server (serverstats_<name>.csv file must exist!)")
async def statsserverduration(interaction, server_name: str):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await interaction.response.send_message("Displaying statistics of "+server_name+" by the longest duration...")
    await serverstats.calculateServerMapStatLongestDuration(interaction, server_name)

#Bot command to reorganise serverstats csv by most sessions
@tree.command(name = "statsserversessions", description = "Display map statistics of a given server by the most sessions played", guild=discord.Object(id=guild_id))
@app_commands.describe(server_name="Name of server (serverstats_<name>.csv file must exist!)")
async def statsserversessions(interaction, server_name: str):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await interaction.response.send_message("Displaying statistics of "+server_name+" by most sessions played...")
    await serverstats.calculateServerMapStatMostSessions(interaction, server_name)

#Bot command to display stats of a specific map on a server
@tree.command(name = "statsservermap", description = "Display statistics of a specific map on a given server", guild=discord.Object(id=guild_id))
@app_commands.describe(server_name="Name of server to get statistics for")
@app_commands.describe(map_name="Name of map to get statistics for")
async def statsservermap(interaction, server_name: str, map_name: str):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await interaction.response.send_message("Displaying statistics of "+map_name+" on "+server_name+"...")
    await serverstats.calculateServerMapStat(interaction, server_name, map_name)

#Bot command to check the length of a map name
@tree.command(name = "checkmapnamelength", description = "Display statistics of a specific map on a given server", guild=discord.Object(id=guild_id))
@app_commands.describe(map_name="Name of the map")
async def checkmapnamelength(interaction, map_name: str):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await formatting.checkCharLimit(interaction, map_name)

#Bot command to test map images
@tree.command(name = "testmapimages", description = "Test map images (only in .jpg format) in embed format found under /testimg/ folder directory", guild=discord.Object(id=guild_id))
@app_commands.describe(map_name="Name of the map without any end suffixes")
async def testmapimages(interaction, map_name: str=None):
    if(interaction.channel.name != 'dev'):
        await interaction.response.send_message(content='Please use this command in the <#'+dev_channel_id+'> channel!')
        return
    await mapimg.testMapImages(interaction, map_name)

#Bot command to choose random guns
@tree.command(name = "randomgun", description = "choose random guns", guild=discord.Object(id=guild_id))
async def randomgun(interaction):
    prim = ["MP9", "MAC-10", "PP-Bizon", "MP7", "MP5-SD", "UMP-45", "P90", "FAMAS", "Galil AR", "M4A4", "M4A1-S", "AK-47", "AUG", "SG 553", "M249"]
    sec = ["SSG 08", "AWP", "SCAR-20", "G3SG1", "Nova", "XM1014", "MAG-7", "Sawed-Off"]
    pistol = ["P2000", "USP-S", "Glock-18", "P250", "Five-seveN", "Tec-9", "CZ75-Auto", "Dual Berettas", "Deagle", "R8 Revolver"]
    await interaction.response.send_message(content='Primary gun: '+prim[np.random.randint(0,len(prim))]+"\nSecondary gun: "+sec[np.random.randint(0,len(sec))]+"\nPistol: "+pistol[np.random.randint(0,len(pistol))])

#Mostly to sync commands after making modifications
@client.event
async def on_message(message):
    #Return if bot is talking to himself
    if message.author == client.user:
        return
    if message.content.startswith('!sync'):
        await tree.sync(guild=discord.Object(id=guild_id))
        await message.channel.send('Syncing commands...')

#Fires when bot is online
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run('put your bot token here')