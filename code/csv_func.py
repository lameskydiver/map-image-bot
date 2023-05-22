import csv
import conversions

csv.field_size_limit(100000000)

#Create a dictionary for each map
def createMapDict(map_name):
    dictionary = {  "name": map_name,
                    "timestamp":[],
                    "duration":[],
                    "players":[],
                    "servercap":[],
                    "score":0.0,
                    "url":""}
    return dictionary

#Modify keyvalues within a dictionary with a provided input
#input should have format of ["ze_name",["keyvalue","value"],["keyvalue2","value2"],...]
def modifyMapDict(dictionary, input):
    for i, row in enumerate(dictionary):
        if (row["name"].lower() == input[0].lower()):
            input.pop(0)
            for values in input:
                if(values[0]=="duration" or values[0]=="players" or values[0]=="servercap" or values[0]=="timestamp"):
                    dictionary[i][values[0]].append(values[1])
                else:
                    dictionary[i][values[0]] = values[1]
            break
    return dictionary

#Returns if a map already exists as a dictionary (no need to create new dictionary)
def findMapDictDuplicate(dictionary, name):
    for row in dictionary:
        if(row["name"].lower()==name.lower()):
            return True
    return False

#Creates csv file for a given server name
def createCSV(name,data,timestamp_start,timestamp_end,header):
    with open(name+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['#'+timestamp_start,timestamp_end])
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
    print("INFO: "+name+".csv successfully created")

#Reform the input csv to display mapname, player count, play duration, and validity of map image url
def reformCsv(data, csv_name):
    timestamps = ''
    zero_players = []
    invalid_playtime = []
    try:
        with open(csv_name+'.csv', 'r', newline='') as file:
            data_row = []
            prev_timestamp = ''
            prev_playercount = -1
            prev_duration = 15
            reader = csv.reader(file)
            for row in reader:
                if (row[0][0]=='%'):
                    continue
                if(row[0][0]=='#'):
                    timestamps = row
                    timestamps[0] = timestamps[0][1:]
                    continue
                if(prev_timestamp==''):
                    prev_timestamp = row[1]
                else:
                    prev_playercount = data_row[1][1]
                    play_time = conversions.findTimeDelta(prev_timestamp,row[1])
                    #Reduce play time for server downtime / server offseason times
                    if((play_time>45 and conversions.serverPopPercentage(data_row[1][1],data_row[2][1])<0.1) or (play_time>90 and conversions.serverPopPercentage(data_row[1][1],data_row[2][1])<0.25) or (play_time>60*6)):
                        #print('INFO: reducing playtime for '+data_row[0]+' ('+data_row[3][1]+')'); removed due to spam in console / not relevant
                        if(round((15+prev_duration)/2) < play_time):
                            invalid_playtime.append([data_row[0],data_row[3][1],str(data_row[1][1])+'/'+str(data_row[2][1]),play_time,prev_duration,round((15+prev_duration)/2)])
                            play_time = round((15+prev_duration)/2)
                        else:
                            invalid_playtime.append([data_row[0],data_row[3][1],str(data_row[1][1])+'/'+str(data_row[2][1]),play_time,prev_duration,play_time])
                    data_row.append(["duration",play_time])
                    prev_timestamp = row[1]
                    if not(findMapDictDuplicate(data,data_row[0])):
                        dictionary = createMapDict(data_row[0])
                        data.append(dictionary)
                    data = modifyMapDict(data, data_row)
                    prev_duration = play_time
                data_row = []
                mapname, player_count, server_cap = conversions.yieldMapNameAndPlayerCount(row[2])
                #If the server is reported 'empty', find out if it really is or just a query glitch by referring to the previous map
                if(player_count==0 and prev_playercount!=-1):
                    zero_players.append([mapname,row[1][:16].replace('T',' '),prev_playercount])
                    player_count = round(prev_playercount * 0.75)
                    #If it still returns 0, set the player count to at least 1
                    if (player_count==0):
                        player_count = 1
                data_row.append(mapname)
                data_row.append(["players",player_count])
                data_row.append(["servercap",server_cap])
                data_row.append(["timestamp",row[1][:16].replace('T',' ')])
                data_row.append(["url",row[0]])
        print('INFO: edited formatting in '+csv_name+'.csv.')
    except:
        print('ERROR: could not find '+csv_name+'.csv!')
    if(invalid_playtime):
        print('INFO: reduced play time for some maps. Refer to '+csv_name+'_invtime.csv for more info.')
        createCSV(csv_name+'_invtime',invalid_playtime,'','',['%'+'name', 'timestamp', 'players','prev duration','prev map duration','modified duration'])
    if(zero_players):
        print('INFO: 0 players detected for some maps. Refer to '+csv_name+'_zeroplyrs.csv for more info.')
        createCSV(csv_name+'_zeroplyrs',zero_players,'','',['%'+'name', 'timestamp', 'prev map players'])
    return data, timestamps