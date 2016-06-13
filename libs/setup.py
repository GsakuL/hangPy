# -*- coding: utf-8 -*-
#(c) Copyright 2016 LukeSkywalk3r
import os, sys, json, time
lang={}
words={}
score={}
gibbet={}

def constrain(minV,cVal,maxV):
    return min(maxV,max(minV,cVal))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def printXY(strIn,xIn,yIn):
    printXYraw(strIn+"\n",xIn,yIn)
    
def printXYraw(strIn,xIn,yIn):
    print("\033["+str(yIn)+";"+str(xIn)+"H"+strIn,end="")

def tobool(inp):
    if str(inp).lower() in {"yes","y","true","t","1"}:
        return True
    return False

def yn(inp):
    if inp:
        return "Yes"
    return "No"



def loadGibbet():
    try:
        global gibbet
        f=open(os.path.join("res","gibbet.json"),"r")
        gibbet=json.load(f)
        f.close()
    except:
        print("ERROR LOADING gibbet.json")
        input()
        sys.exit()
        
def loadConfig():
    try:
        global config
        f=open(os.path.join("res","config.json"),"r")
        config=json.load(f)
        f.close()
    except:
        print("ERROR LOADING config.json")
        input()
        sys.exit()
        
def loadScore():
    try:
        global score
        f=open(os.path.join("res","score.json"),"r")
        score=json.load(f)
        f.close()
    except:
        print("ERROR LOADING score.json")
        input()
        sys.exit()
        
loadGibbet()
loadConfig()
loadScore()

try:
    maxFrames=int(gibbet["properties"]["frames"])
except:
    maxFrames=0
    for i in gibbet["art"]:    
        maxFrames=maxFrames+1
    gibbet["properties"]["frames"]=int(maxFrames)
    maxFrames=None
    
    

try:
    maxLines=int(gibbet["properties"]["lines"])
except:
    maxLines=0

    for i in gibbet["art"]:
        count=0
        for j in gibbet["art"][i]:
            count=count+1
        maxLines=max(maxLines,count)
    gibbet["properties"]["lines"]=int(maxLines)
    maxLines=None

try:
    maxLen=int(gibbet["properties"]["maxlen"])
except:
    maxLen=0
    for i in gibbet["art"]:
        for j in gibbet["art"][i]:
            maxLen=max(maxLen,len(gibbet["art"][i][j]))
    gibbet["properties"]["maxlen"]=int(maxLen)
    maxLen=None


f=None

def loadLang():
    langFiles=[]
    langFiles.clear()
    for tFile in os.listdir("lang"):
        if tFile.endswith(".json"):
            langFiles.append(tFile)

    for tFile in langFiles:
        f=open(os.path.join("lang",tFile),"r")

        lang[tFile.split(".")[0]]=json.load(f)
        f.close()
        f=None
        
def loadWords():
    wordFiles=[]
    wordFiles.clear()
    for tFile in os.listdir("words"):
        if tFile.endswith(".json"):
            wordFiles.append(tFile)
        
    for tFile in wordFiles:
        f=open(os.path.join("words",tFile),"r")
        #global lang

        words[tFile.split(".")[0]]=json.load(f)
        f.close()
        f=None
    
    for i in words:
        words[i]["entries"]=len(words[i]["words"])
loadLang()
loadWords()
def printGibbetState(stateIndex,posX=-1,posY=-1):
    j=0
    i=0
    if posY>=0 and posX>=0 and type(posX)==int and type(posY)==int:
        for i in range(0,int(float(gibbet["properties"]["lines"]))):
            printXY(gibbet["art"]["step_"+str(stateIndex)]["line_"+str(i)],posX,posY)
            i+=1
    else:
        for i in range(0,int(float(gibbet["properties"]["lines"]))):
            print(gibbet["art"]["step_"+str(stateIndex)]["line_"+str(i)])
            i+=1
            
def saveConfig():
    global config
    f=open(os.path.join("res","config.json"),"w")
    json.dump(config,f,indent=4)
    f.close()
    
def saveScore():
    global score
    f=open(os.path.join("res","score.json"),"w")
    json.dump(score,f,indent=4)
    f.close()
    
def scoreAddLang(langName):
    global score
    try:
        if  score[langName]==None:
             score[langName]={}
    except:
        if not('score['+langName+']' in vars()):
            score[langName]={}
            
def scoreAddWord(langName,vWord):
    try:
        if score[langName][vWord]==None:
            score[langName][vWord]={}
    except:
        if not('score['+langName+']['+vWord+']' in vars()):
            score[langName][vWord]={}
            
def checkScoreStats(langName,vWord,usrName,tries,timeNeed,dateTime,guessedWord,gameState,gameScore):
    newEntry=False
    try:
        if score[langName][vWord][usrName]==None:
            newEntry=True
    except:
        if not('score['+langName+']['+vWord+']['+usrName+']' in vars()):
            newEntry=True
    if not(newEntry):
        if (score[langName][vWord][usrName]["game_state"]==gameState and score[langName][vWord][usrName]["game_score"]>gameScore) or (score[langName][vWord][usrName]["game_state"]=="loose" and "win" == gameState):
            newEntry=True
    if newEntry:
        scoreAddStats(langName,vWord,usrName,tries,timeNeed,dateTime,guessedWord,gameState,gameScore)
    
def scoreAddStats(langName,vWord,usrName,tries,timeNeed,dateTime,guessedWord,gameState,gameScore):
    score[langName][vWord][usrName]={}
    score[langName][vWord][usrName]["tries"]=tries
    score[langName][vWord][usrName]["guessed_word"]=guessedWord
    score[langName][vWord][usrName]["date"]=dateTime
    score[langName][vWord][usrName]["time_needed"]=timeNeed
    score[langName][vWord][usrName]["game_state"]=gameState
    score[langName][vWord][usrName]["game_score"]=gameScore

def addToHighscore(dictLang,usrWord,usrName,tries,timeNeed,dateTime,guessedWord,gameState,gameScore):
    global score
    scoreAddLang(dictLang)
    scoreAddWord(dictLang,usrWord)
    checkScoreStats(dictLang,usrWord,usrName,tries,timeNeed,dateTime,guessedWord,gameState,gameScore)  
    saveScore()
    
def getLang(typeIn):
    if typeIn.lower()=="ui":
        return config["user"]["lastUiLang"]
    else:
        if config["user"]["lastDictLang"] in {"auto", "ui"}:
            return config["user"]["lastUiLang"]
    return config["user"]["lastDictLang"]
