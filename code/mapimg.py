import discord
import csv_func
import csv
import conversions
import formatting
import suffix
from datetime import datetime

#Record map tracking data from a given date and time input
async def recordMapTrackEmbed(interaction, channel, timestamp_start, timestamp_end):
    if(datetime.fromisoformat(timestamp_end+'+00:00') < datetime.fromisoformat(timestamp_start+'+00:00')):
        await interaction.edit_original_response(content = "The ending timestamp (*"+timestamp_end+"*) cannot be earlier than the starting timestamp (*"+timestamp_start+"*)")
        return
    #await interaction.response.send_message("Working...")
    data = []
    async for message in channel.history(limit=None, before=datetime.fromisoformat(timestamp_end+'+00:00'), after=datetime.fromisoformat(timestamp_start+'+00:00')):
        if(message.embeds):
            if(message.embeds[0].to_dict()['description'].find('Currently Playing')!=-1):
                continue
            map_data = []
            map_data.append(message.embeds[0].to_dict()['thumbnail']['url'])
            map_data.append(message.embeds[0].to_dict()['timestamp'])
            desc = message.embeds[0].to_dict()['description'].replace('\\_','_')
            map_data.append(desc.replace('\n',' '))
            data.append(map_data)
    if not (data):
        await interaction.channel.send(content="No map tracks records has been found in between the given timestamps of ***"+timestamp_start+"*** and ***"+timestamp_end+"*** for the server **"+channel.name+"**. Make sure the timestamps is formatted for UTC+0.")
    else:
        await interaction.channel.send(content="There were **"+str(len(data))+"** valid map tracks for the server **"+channel.name+"**.")
    csv_func.createCSV(channel.name,data,timestamp_start,timestamp_end,['%'+'url', 'timestamp', 'description'])

#Find map tracks with missing images
def consolidateInvalidMapImg(data,csv_name):
    old_data = data[:]
    data,dummy = csv_func.reformCsv(data,csv_name)
    if (data==old_data or data==[]):
        print("ERROR: no data has been recorded on "+csv_name+"!")
        return old_data
    new_data = [row for row in data if row["url"].find('https://vauff.com/mapimgs/730/')==-1]
    if (old_data==new_data):
        print("INFO: no (additional) missing map image has been recorded on "+csv_name+"!")
        return old_data
    return new_data

def mergeDict(array, dict_add):
    idx = [i for i,_ in enumerate(array) if _['name']==dict_add['name']][0]
    for kv in dict_add:
        if(kv == 'name' or kv == 'url' or kv == 'score'):
            continue
        elif (kv == 'suffix'):
            if (dict_add['suffix'][0] not in array[idx]['suffix']):
                array[idx]['suffix'].append(dict_add['suffix'][0])
        else:
            array[idx][kv].append(dict_add[kv][0])
    return array

def combineMaps(data):
    consolidated = []
    for i in range(len(data)):
        name, suff = suffix.findSuffix(data[i]["name"][:3],data[i]["name"][3:])
        data[i]['name'] = name
        data[i]['suffix'].append(suff)
        if name in [x['name'] for x in consolidated]:
            mergeDict(consolidated, data[i])
        else:
            consolidated.append(data[i])
    return consolidated

#Maps to avoid as their bsp cannot be found anywhere online or crashes the game on load
g_avoid = [ "zr_abandoned_hospital_csgo_v10"    ,
            "zr_devious_office_csgo_v16"        ,
            "ze_surgical_nightmare_v1_b2c"      ,
            "ze_100traps_v4_1_nc1"              ,
            "ze_hive_complex_v1_2_1"      ]

#Merge mapimg csv files for all tracked servers to determine prioritised list of missing map images
async def analyseMapImg(interaction, data, csv_name):
    data = combineMaps(data)
    for it, row in enumerate(data):
        data[it]["score"] = conversions.calculateScore(row)
    data.sort(key=lambda x: x["name"].lower())
    data.sort(key=lambda x: x["score"], reverse=True)
    data = removeInvalidMaps(data)
    max_length = formatting.maxLength(data,["","name","avgplayers","duration","sessions","score"],['rank', 'name', 'avg players', 'tot playtime', 'num sessions', 'score'])
    with open('mapimg_'+csv_name+'.csv', 'w', newline='') as temp:
        writer = csv.writer(temp)
        writer.writerow(formatting.fillBlank(['rank', 'name', 'avg players', 'tot playtime', 'num sessions', 'score'],max_length))
        for i, row in enumerate(data):
            writer.writerow(formatting.fillBlank([str(i+1)+')', row["name"],str(round(float(sum(row["players"]))/float(len(row["timestamp"]))))+'/'+str(round((float(sum(row["servercap"]))/float(len(row["timestamp"]))))),sum(row["duration"]),len(row["timestamp"]),row["score"]],max_length))
        writer.writerow(['#----raw data----'])
        writer.writerow([data])
    text = ''
    for i, row in enumerate(data):
        #Only return maps with top 15 scores
        if(i>14):
            break
        if(len(row["name"])>31):
            text = text + row["name"] + " ***(31 char warning)***\n"
        else:
            text = text + row["name"] + '\n'
    map_embed = discord.Embed(title="Prioritised list of maps without proper image", description=text)
    await interaction.edit_original_response(content='',embed=map_embed)

#Remove maps defined in g_avoid
def removeInvalidMaps(data):
    data = [row for row in data if (row["name"] not in g_avoid[:])]
    return  data

#Test map images in the embed format
async def testMapImages(interaction, map_name):
    images = os.listdir('testimg/')#for getting all files n folder in the current path
    it = 1
    embeds_q = []
    files_q = []
    if(map_name==None):
        map_name = "ze_test_map"
    map_name += "_t"
    for i in images:
        i = "testimg/"+i
        if(i[i.find(".")+1:]=="jpg"):
            try:
                #print(i)
                files_q.append(discord.File(i,filename=map_name+str(it)+'.jpg'))
                desc = "Now Playing: **"+map_name+str(it)+"**\nPlayers Online: **64/64**\nQuick Join: ** [example.zombie.server:27040](http://vauff.com/?ip=example.zombie.server:27040)**"
                rgb = colour.findAvgRGB(i,10)
                embed = discord.Embed(description=desc,colour=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
                embed.set_thumbnail(url="attachment://"+map_name+str(it)+".jpg")
                embeds_q.append(embed)
                it += 1
            except:
                await interaction.response.send_message(content="Error has occurred.")
                return
    if(len(embeds_q)==0):
        await interaction.response.send_message(content="No valid images have been found in the directory.")
    else:
        await interaction.response.send_message(files=files_q,embeds=embeds_q)