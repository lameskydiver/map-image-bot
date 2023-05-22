#Finds the time difference between two given timestamps
def findTimeDelta(init_timestamp, end_timestamp):
    init_date = init_timestamp[:init_timestamp.find('T')]
    init_time = init_timestamp[init_timestamp.find('T')+1:init_timestamp.find('T')+6]
    end_date = end_timestamp[:end_timestamp.find('T')]
    end_time = end_timestamp[end_timestamp.find('T')+1:end_timestamp.find('T')+6]
    delta = (int(end_time[:2])*60+int(end_time[3:]))-(int(init_time[:2])*60+int(init_time[3:]))
    if(init_date!=end_date):
        delta = delta + 60*24
    return delta

#Calculates the percentage of players online versus total server capacity
def serverPopPercentage(player_count,server_cap):
    return float(player_count)/float(server_cap)

#Determine map name and player count from a given string
def yieldMapNameAndPlayerCount(string):
    mapname = string[15:string.find('**',14)]
    player_count = string[string.find('Online: **')+10:string.find('**',string.find('Online: **')+10)]
    server_cap = int(player_count[player_count.find('/')+1:])
    player_count = int(player_count[:player_count.find('/')])
    return mapname, player_count, server_cap

#Determine the score of the given input (map) dictionary
def calculateScore(dictionary):
    score = []
    for i,j,k in zip(dictionary["players"],dictionary["servercap"],dictionary["duration"]):
        score.append(serverPopPercentage(i,j)*k)
    return round(sum(score),2)

#Calculate total amount of map tracks recorded
def calculateServerTotSessions(dictionaries):
    tot_sessions = 0
    for row in dictionaries:
        tot_sessions += len(row["timestamp"])
    return tot_sessions

#Calculate average amount of players of the entire map tracking data
def calculateServerAvgPlayer(dictionaries, tot_sessions):
    tot_players = 0
    tot_capacity = 0
    for row in dictionaries:
        tot_players += sum(row["players"])
        tot_capacity += sum(row["servercap"])
    return str(round(float(tot_players)/float(tot_sessions)))+'/'+str(round(float(tot_capacity)/float(tot_sessions)))

#Calculate average time server stays on a map
def calculateServerAvgMapDuration(dictionaries, tot_sessions):
    tot_duration = 0
    for row in dictionaries:
        tot_duration += sum(row["duration"])
    return round(tot_duration/tot_sessions)