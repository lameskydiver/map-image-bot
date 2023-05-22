#Determines the length of the longest string per column of a nested dictionaries (adds extra space at end)
def maxLength(data, vars, header):
    maxlength = [1] * len(vars)
    for i, row in enumerate(header):
        maxlength[i] = len(row)+1
    for row in data:
        for i,var_row in enumerate(vars):
            if(var_row=="name"):
                if(len(str(row[var_row]))+1>maxlength[i]):
                    maxlength[i] = len(str(row[var_row]))+1
            else:
                continue
    return maxlength

#Adds blank space to a row of string with given conditions
def fillBlank(row, maxlength):
    for i, element in enumerate(row):
        row[i] = str(element) + ' '*(maxlength[i]-int(len(str(element))))
    return row

#Returns the length of the map name and a trimmed name under 31 chars for vauff.com
async def checkCharLimit(interaction, input):
    length = len(input)
    if(length > 31):
        await interaction.response.send_message(content="`"+input+"` has "+str(length)+" characters.\n`"+input[:31]+"` for the 31 characters limit")
    else:
        await interaction.response.send_message(content="`"+input+"` has "+str(length)+" characters.")
