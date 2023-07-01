import discord
import csv_func
import csv
import formatting
import conversions
import colour

#Calculate the overall server statistics
async def calculateServerStat(interaction, server_name):
    data = []
    data,record_timestamps = csv_func.reformCsv(data, server_name)
    if(data == []):
        await interaction.edit_original_response(content=server_name+".csv does not exist yet! Make sure to create this file first, or check if you have made any typos!")
        return
    tot_sessions = conversions.calculateServerTotSessions(data)
    tot_unique_sessions = len(data)
    avg_players = conversions.calculateServerAvgPlayer(data, tot_sessions)
    avg_duration = conversions.calculateServerAvgMapDuration(data, tot_sessions)
    for it, row in enumerate(data):
        data[it]["score"] = conversions.calculateScore(row)
    data.sort(key=lambda x: x["name"].lower())
    data.sort(key=lambda x: x["score"], reverse=True)
    max_length = formatting.maxLength(data,["","name","avgplayers","duration","sessions","score"],['rank', 'name', 'avg players', 'tot playtime', 'num sessions', 'score'])
    with open('serverstats/serverstats_'+server_name+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['========================================'])
        writer.writerow(['Server statistics for '+server_name])
        writer.writerow(['Data recorded from '+record_timestamps[0]+' (UTC+0) to '+record_timestamps[1]+' (UTC+0)'])
        writer.writerow(['--------------------'])
        writer.writerow(['Total number of sessions: '+str(tot_sessions)])
        writer.writerow(['Total amount of unique maps played: '+str(tot_unique_sessions)])
        writer.writerow(['Average player count: '+avg_players])
        writer.writerow(['Average duration per map: '+str(avg_duration)+' minutes'])
        writer.writerow(['========================================'])
        writer.writerow(['* Map score calculated by: sigma_(sessions)^(all sessions) (player count on session/server capacity on session) * map duration on session'])
        writer.writerow(['    i.e. map score is weighted by player count and duration played per each session'])
        writer.writerow(['* Play duration is in minutes'])
        writer.writerow(['========================================'])
        writer.writerow(formatting.fillBlank(['rank', 'name', 'avg players', 'tot playtime', 'num sessions', 'score'],max_length))
        for i, row in enumerate(data):
            writer.writerow(formatting.fillBlank([str(i+1)+')', row["name"],str(round(float(sum(row["players"]))/float(len(row["timestamp"]))))+'/'+str(round((float(sum(row["servercap"]))/float(len(row["timestamp"]))))),sum(row["duration"]),len(row["timestamp"]),row["score"]],max_length))
        writer.writerow(['#----raw data----'])
        writer.writerow([data])
        writer.writerow(record_timestamps)
    text = ''
    for i, row in enumerate(data):
        #Only return maps with top 10 scores
        if(i>9):
            break
        text = text + row["name"] + '\n'
    if data[0]["url"].find('https://vauff.com/mapimgs/730/')!=-1:
        rgb = colour.findAvgRGB(data[0]["url"],10)
    else:
        rgb = [0,154,255]
    map_embed = discord.Embed(title="The top 10 popular maps in "+server_name, description=text, colour=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
    map_embed.set_footer(text="Map rank is calculated by: summation of all sessions of [(session player count/ session server total capacity) x session map playtime]")
    map_embed.set_author(name="From "+record_timestamps[0]+" (UTC+0) to "+record_timestamps[1]+" (UTC+0)")
    map_embed.add_field(name='Total sessions',value=tot_sessions)
    map_embed.add_field(name='Total unique maps',value=tot_unique_sessions)
    map_embed.add_field(name='Average player count',value=avg_players)
    map_embed.add_field(name='Average map duration',value=str(avg_duration)+' minutes')
    map_embed.set_thumbnail(url=data[0]["url"])
    await interaction.edit_original_response(embed=map_embed)

#List server stats in terms of longest total duration
async def calculateServerMapStatLongestDuration(interaction, server_name):
    data = []
    start_record = False
    try:
        with open('serverstats/serverstats_'+server_name+'.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if(row[0][0]!="#" and start_record == False):
                    continue
                if(start_record==True):
                    if(data==[]):
                        data = list(eval(row[0]))
                    else:
                        record_timestamps = row
                else:
                    start_record = True
        data.sort(key=lambda x: int(sum(x["duration"])), reverse=True)
        tot_sessions = conversions.calculateServerTotSessions(data)
        tot_unique_sessions = len(data)
        avg_players = conversions.calculateServerAvgPlayer(data, tot_sessions)
        avg_duration = conversions.calculateServerAvgMapDuration(data, tot_sessions)
        text = ''
        for i, row in enumerate(data):
            #Only return maps with top 10 scores
            if(i>9):
                break
            text = text + row["name"] + '\n'
        if data[0]["url"].find('https://vauff.com/mapimgs/730/')!=-1:
            rgb = colour.findAvgRGB(data[0]["url"],10)
        else:
            rgb = [0,154,255]
        map_embed = discord.Embed(title="The top 10 longest played maps in "+server_name, description=text, colour=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
        map_embed.set_author(name="From "+record_timestamps[0]+" (UTC+0) to "+record_timestamps[1]+" (UTC+0)")
        map_embed.add_field(name='Total sessions',value=tot_sessions)
        map_embed.add_field(name='Total unique maps',value=tot_unique_sessions)
        map_embed.add_field(name='Average player count',value=avg_players)
        map_embed.add_field(name='Average map duration',value=str(avg_duration))
        map_embed.set_thumbnail(url=data[0]["url"])
        await interaction.edit_original_response(embed=map_embed)
        max_length = formatting.maxLength(data,["","name","avgplayers","duration","sessions"],['rank', 'name', 'avg players', 'tot playtime', 'num sessions'])
        with open('serverstats/serverstats_'+server_name+'_duration.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['========================================'])
            writer.writerow(['Server statistics for '+server_name+' by longest duration'])
            writer.writerow(['Data recorded from '+record_timestamps[0]+' (UTC+0) to '+record_timestamps[1]+' (UTC+0)'])
            writer.writerow(['--------------------'])
            writer.writerow(['Total number of sessions: '+str(tot_sessions)])
            writer.writerow(['Total amount of unique maps played: '+str(tot_unique_sessions)])
            writer.writerow(['Average player count: '+avg_players])
            writer.writerow(['Average duration per map: '+str(avg_duration)+' minutes'])
            writer.writerow(['========================================'])
            writer.writerow(['* Play duration is in minutes'])
            writer.writerow(['========================================'])
            writer.writerow(formatting.fillBlank(['rank', 'name', 'avg players', 'tot playtime', 'num sessions'],max_length))
            for i, row in enumerate(data):
                writer.writerow(formatting.fillBlank([str(i+1)+')', row["name"],str(round(float(sum(row["players"]))/float(len(row["timestamp"]))))+'/'+str(round((float(sum(row["servercap"]))/float(len(row["timestamp"]))))),sum(row["duration"]),len(row["timestamp"])],max_length))
            writer.writerow(['#----raw data----'])
            writer.writerow([data])
            writer.writerow(record_timestamps)
    except:
        await interaction.edit_original_response(content="serverstats_"+server_name+".csv has not been found. Please ensure this file exists beforehand!")

#List server stats in terms of most sessions
async def calculateServerMapStatMostSessions(interaction, server_name):
    data = []
    start_record = False
    try:
        with open('serverstats/serverstats_'+server_name+'.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if(row[0][0]!="#" and start_record == False):
                    continue
                if(start_record==True):
                    if(data==[]):
                        data = list(eval(row[0]))
                    else:
                        record_timestamps = row
                else:
                    start_record = True
        data.sort(key=lambda x: int(len(x["timestamp"])), reverse=True)
        tot_sessions = conversions.calculateServerTotSessions(data)
        tot_unique_sessions = len(data)
        avg_players = conversions.calculateServerAvgPlayer(data, tot_sessions)
        avg_duration = conversions.calculateServerAvgMapDuration(data, tot_sessions)
        text = ''
        for i, row in enumerate(data):
            #Only return maps with top 10 scores
            if(i>9):
                break
            text = text + row["name"] + '\n'
        if data[0]["url"].find('https://vauff.com/mapimgs/730/')!=-1:
            rgb = colour.findAvgRGB(data[0]["url"],10)
        else:
            rgb = [0,154,255]
        map_embed = discord.Embed(title="The top 10 most frequently played maps in "+server_name, description=text, colour=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
        map_embed.set_author(name="From "+record_timestamps[0]+" (UTC+0) to "+record_timestamps[1]+" (UTC+0)")
        map_embed.add_field(name='Total sessions',value=tot_sessions)
        map_embed.add_field(name='Total unique maps',value=tot_unique_sessions)
        map_embed.add_field(name='Average player count',value=avg_players)
        map_embed.add_field(name='Average map duration',value=str(avg_duration))
        map_embed.set_thumbnail(url=data[0]["url"])
        await interaction.edit_original_response(embed=map_embed)
        max_length = formatting.maxLength(data,["","name","avgplayers","duration","sessions"],['rank', 'name', 'avg players', 'tot playtime', 'num sessions'])
        with open('serverstats/serverstats_'+server_name+'_sessions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['========================================'])
            writer.writerow(['Server statistics for '+server_name+' by most sessions'])
            writer.writerow(['Data recorded from '+record_timestamps[0]+' (UTC+0) to '+record_timestamps[1]+' (UTC+0)'])
            writer.writerow(['--------------------'])
            writer.writerow(['Total number of sessions: '+str(tot_sessions)])
            writer.writerow(['Total amount of unique maps played: '+str(tot_unique_sessions)])
            writer.writerow(['Average player count: '+avg_players])
            writer.writerow(['Average duration per map: '+str(avg_duration)+' minutes'])
            writer.writerow(['========================================'])
            writer.writerow(['* Play duration is in minutes'])
            writer.writerow(['========================================'])
            writer.writerow(formatting.fillBlank(['rank', 'name', 'avg players', 'tot playtime', 'num sessions'],max_length))
            for i, row in enumerate(data):
                writer.writerow(formatting.fillBlank([str(i+1)+')', row["name"],str(round(float(sum(row["players"]))/float(len(row["timestamp"]))))+'/'+str(round((float(sum(row["servercap"]))/float(len(row["timestamp"]))))),sum(row["duration"]),len(row["timestamp"])],max_length))
            writer.writerow(['#----raw data----'])
            writer.writerow([data])
            writer.writerow(record_timestamps)
    except:
        await interaction.edit_original_response(content="serverstats_"+server_name+".csv has not been found. Please ensure this file exists beforehand!")

#Calculate the statistics of a map on a server
async def calculateServerMapStat(interaction, server_name, map_name):
    data = []
    try:
        with open('serverstats/serverstats_'+server_name+'.csv', 'r', newline='') as file:
            start_record = False
            reader = csv.reader(file)
            temp = []
            for row in reader:
                if(row[0][0]!="#" and start_record == False):
                    continue
                if(start_record==True):
                    if(temp==[]):
                        temp = list(eval(row[0]))
                        for dict_row in temp:
                            if(dict_row["name"].lower()==map_name.lower()):
                                data.append(dict_row)
                    else:
                        record_timestamps = row
                else:
                    start_record = True
    except:
        await interaction.edit_original_response(content="Error has occurred. Please ensure that both the server name and the map name are correct")
        return
    if(data==[]):
        await interaction.edit_original_response(content="No map track record has been recorded for "+map_name+". A longer server tracking record may be required, or potentially a typo/different map version than what is present on "+server_name)
        return
    tot_sessions = conversions.calculateServerTotSessions(data)
    avg_players = conversions.calculateServerAvgPlayer(data, tot_sessions)
    avg_duration = conversions.calculateServerAvgMapDuration(data, tot_sessions)
    duration = sum(data[0]["duration"])
    player_text = ''
    for i in range(len(data[0]["players"])):
        player_text += str(data[0]["players"][i])+'/'+str(data[0]["servercap"][i])+'\n'
    if data[0]["url"].find('https://vauff.com/mapimgs/730/')!=-1:
        rgb = colour.findAvgRGB(data[0]["url"],10)
    else:
        rgb = [0,154,255]
    map_embed = discord.Embed(title="Statistics of "+map_name+" on "+server_name, colour=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
    map_embed.set_author(name="From "+record_timestamps[0]+" (UTC+0) to "+record_timestamps[1]+" (UTC+0)")
    map_embed.add_field(name='Timestamps (UTC+0)',value=str(data[0]["timestamp"])[1:-1].replace(",","\n").replace("'",""))
    map_embed.add_field(name='Players Online',value=player_text)
    map_embed.add_field(name='Total Duration (mins)',value=str(data[0]["duration"])[1:-1].replace(",","\n"))
    map_embed.set_thumbnail(url=data[0]["url"])
    await interaction.edit_original_response(embed=map_embed)
    max_length = formatting.maxLength(data,["timestamp","avgplayers","duration"],['timestamp', 'players', 'playtime'])
    with open('serverstats/serverstats_'+server_name+'_'+map_name+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['========================================'])
        writer.writerow(['Map statistics for '+map_name+' on '+server_name])
        writer.writerow(['Data recorded from '+record_timestamps[0]+' (UTC+0) to '+record_timestamps[1]+' (UTC+0)'])
        writer.writerow(['--------------------'])
        writer.writerow(['Total number of sessions: '+str(tot_sessions)])
        writer.writerow(['Average player count: '+avg_players])
        writer.writerow(['Total duration of the map: '+str(duration)+' minutes'])
        writer.writerow(['Average duration per session: '+str(avg_duration)+' minutes'])
        writer.writerow(['========================================'])
        writer.writerow(['* Play duration is in minutes'])
        writer.writerow(['========================================'])
        writer.writerow(formatting.fillBlank(['timestamp (utc+0)', 'players', 'playtime'],max_length))
        for i in range(len(data[0]["timestamp"])):
            writer.writerow(formatting.fillBlank([data[0]["timestamp"][i], str(data[0]["players"][i])+'/'+str(data[0]["servercap"][i]),data[0]["duration"][i],],max_length))
        writer.writerow(['#----raw data----'])
        writer.writerow([data])
        writer.writerow(record_timestamps)