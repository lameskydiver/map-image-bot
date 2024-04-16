def splitStringByUnderscore(s):
    return s[:s.rfind('_')], '_'+s[s.rfind('_')+1:]

def isAlphabet(s):
    return True if (ord(s) >= ord('a') and ord(s) <= ord('z')) else False

def isCapitalAlphabet(s):
    return True if (ord(s) >= ord('A') and ord(s) <= ord('Z')) else False

def isNumeric(s):
    return True if (ord(s) >= ord('0') and ord(s) <= ord('9')) else False

def findDefaultSuffix(ss):
    for i in default_suffix:
        if(ss.find(i) != -1):
            return True
    return False

def testSuffix(ss):
    if(len(ss)==1):
        #Starting with CS2 all map names from maunz bot are small letters, so maps like s_a_m cannot be filtered as easily
        #leaving the capital letter check just in case capital letters do return on maunz bot
        if(isAlphabet(ss.lower()) and (isCapitalAlphabet(ss) or ss != 'p')):
            return False
        else:
            return True
    elif(len(ss)==0):
        return True
    elif(len(ss)<=6):
        if(findDefaultSuffix(ss.lower())):
            return True
        if(isAlphabet(ss[0].lower()) and not isCapitalAlphabet(ss[0])):
            if((isNumeric(ss[-1]) or isNumeric(ss[1]))):
                return True
        if(isNumeric(ss[0])):
            if((isAlphabet(ss[1].lower()) and not isCapitalAlphabet(ss[1])) or (isAlphabet(ss[-1].lower()) and not isCapitalAlphabet(ss[-1]))):
                return True
        try:
            if(int(ss)<30):
                return True
        except:
            return False
    return False

def findSuffix(prefix,name):
    underscores = name.count('_')
    if(underscores == 0):
        return prefix+name, ''
    else:
        s = name[:]
        suff = ''
        while(underscores > 0):
            s, ss = splitStringByUnderscore(s)
            if(testSuffix(ss[1:])):
                suff = ss + suff
            else:
                s += ss
                break
            underscores -= 1
        return prefix+s, suff

default_suffix = ['alpha','beta','final','fix','csgo','go','hdr','test']