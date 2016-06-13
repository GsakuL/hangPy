#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#(c) Copyright 2016 LukeSkywalk3r
import os, sys, time, json, random
from libs.setup import *

gameStats={}
for j in {"userInput", "state", "userWord","enteredLetters"}:
    gameStats[j]=""
    
for j in {"userScore", "userTries"}:
    gameStats[j]=0
    
for j in {"userLetters"}:
    gameStats[j]=" "
    
for j in {"gameEnd","guessedWord"}:
    gameStats[j]=False


def mainMenu():
    while True:
        clear()
        printGibbetState(11)
        printXY(lang[getLang("ui")]["strings"]["title"],gibbet["properties"]["maxlen"]+7,2)
        printXY(lang[getLang("ui")]["strings"]["title_desc"],gibbet["properties"]["maxlen"]+7,3)
        printXY(lang[getLang("ui")]["rights"]["copyright"],gibbet["properties"]["maxlen"]+13,4)
        printXY(lang[getLang("ui")]["strings"]["menu"],gibbet["properties"]["maxlen"]+10,6)
        printXY(lang[getLang("ui")]["strings"]["menu_1"]+" ("+lang[getLang("ui")]["strings"]["dict"]+": "+words[getLang("d")]["properties"]["langName"]+")",gibbet["properties"]["maxlen"]+12,7)
        printXY(lang[getLang("ui")]["strings"]["menu_2"],gibbet["properties"]["maxlen"]+12,8)
        printXY(lang[getLang("ui")]["strings"]["menu_3"],gibbet["properties"]["maxlen"]+12,9)
        printXY(lang[getLang("ui")]["strings"]["menu_help"],gibbet["properties"]["maxlen"]+12,11)
        printXY(lang[getLang("ui")]["strings"]["menu_x"],gibbet["properties"]["maxlen"]+12,12)
        
        printXY(lang[getLang("ui")]["strings"]["enter_to_confirm"],gibbet["properties"]["maxlen"]+12,14)
        
        
        
        printXYraw("]>",0,max(gibbet["properties"]["lines"]+2,15))
        global userInput
        userInput=input().lower().strip("_ ")
        if userInput in {"x","!x","exit"}:
            print(lang[getLang("ui")]["strings"]["goodbye"])
            sys.exit()
        elif userInput in {"?","h"}:
            showHelp()
        elif userInput=="1":
            playGame()
        elif userInput=="2":
            showHighscore()
        elif userInput=="3":
            openOptions()
                
def drawGameBoard():
    global gameStats
    gWord=""
    
    for ch in gameStats["userWord"]:
        if ch in gameStats["userLetters"].upper():
            gWord+=str(ch)+" "
        else:
            gWord+="_ "
    gWord.upper().strip("_ ")
    printXYraw("",0,0)
    printGibbetState(constrain(0,gameStats["userFails"],gibbet["properties"]["frames"]))
    printXY(gWord,gibbet["properties"]["maxlen"]+5,2)
    if config["user"]["show_entered_letters"]:
        printXY(("".join(sorted(set(gameStats["enteredLetters"])))).upper().replace(""," ").strip("_ "),0,gibbet["properties"]["lines"]+2)
    if not(gameStats["userFails"]+1>=gibbet["properties"]["frames"]) and (gameStats["state"]=="play") and(gWord.replace("_","").replace(" ","")==gameStats["userWord"]):
        gameStats["state"]="win"

def drawInputLine():
    printXY(lang[getLang("ui")]["strings"]["enter_a_letter"],0,gibbet["properties"]["lines"]+3)
    printXYraw("]>",0,gibbet["properties"]["lines"]+4)

                
                
def checkInputForWord():
    gameStats["enteredLetters"]="".join(sorted(set(gameStats["enteredLetters"]+gameStats["userInput"])))
    global gameStats
    if gameStats["userInput"]=="!X":
        gameStats["state"]="exit" 
    else:
        if gameStats["userInput"]==gameStats["userWord"]:
            gameStats["state"]="win" 
            gameStats["guessedWord"]=True
            for ch in gameStats["userWord"]:
                if not(ch in gameStats["userLetters"]):
                    gameStats["userScore"]+=2
            gameStats["userScore"]+=5
            
            gameStats["userTries"]+=1
            gameStats["userLetters"]="".join(sorted(set(gameStats["userWord"]+gameStats["enteredLetters"]+gameStats["userLetters"])))
        else:
            for ch in gameStats["userInput"].upper():
                if not(ch in gameStats["userLetters"].upper()):
                    gameStats["userLetters"]+=str(ch)
                    if ch in gameStats["userWord"]:
                        gameStats["userScore"]+=2
                        gameStats["userTries"]+=1
                if not(ch in gameStats["userWord"]):
                    gameStats["userFails"]+=1
                    gameStats["userScore"]-=0.1

            if (gameStats["userFails"]+1>=gibbet["properties"]["frames"]):
                gameStats["state"]="loose"
                gameStats["userFails"]=gibbet["properties"]["frames"]-1
            
def playGame():
    global gameStats
    
    gameStats["state"]="play"
    gameStats["userWord"]=(random.choice(words[getLang("dict")]["words"])).upper()
    if config["user"]["start_with_random_letter"]:
        tmp=random.choice(gameStats["userWord"])
    else:
        tmp=""
    for j in {"enteredLetters","userLetters"}:
        gameStats[j]=" "+tmp
    for j in {"gameEnd","guessedWord"}:
        gameStats[j]=False
    for j in {"userFails","userScore","userTries"}:
        gameStats[j]=0
    
    
    gameTime=time.time() 
    while gameStats["state"] in {"play"}:
        clear()
        drawGameBoard()
        drawInputLine()
        gameStats["userInput"]=input().upper().strip()
        checkInputForWord()
        drawGameBoard()
            
    gameTime=int(time.time()-gameTime)
    
    #game ended
    if not(gameStats["state"] in {"exit"}):
        gameStats["userScore"]=(int(gameStats["userScore"]-(gameTime*0.025))*100)/100
        printXY(lang[getLang("ui")]["strings"][gameStats["state"]],gibbet["properties"]["maxlen"]+5,5)

        printXY(lang[getLang("ui")]["strings"]["score_title"]+" "*300,0,gibbet["properties"]["lines"]+3)
        printXY(lang[getLang("ui")]["strings"]["score_points"]+str(gameStats["userScore"]),0,gibbet["properties"]["lines"]+4)
        printXY(lang[getLang("ui")]["strings"]["score_time"]+str(gameTime)+"s.",0,gibbet["properties"]["lines"]+5)
        printXY(lang[getLang("ui")]["strings"]["score_guessed_word"]+lang[getLang("ui")]["strings"][(yn(tobool(gameStats["guessedWord"]))).lower()],0,gibbet["properties"]["lines"]+6)
        printXY(lang[getLang("ui")]["strings"]["score_tries"]+str(gameStats["userFails"]+gameStats["userTries"]),0,gibbet["properties"]["lines"]+7)

        printXY(lang[getLang("ui")]["strings"]["prompt_highscore_0"],0,gibbet["properties"]["lines"]+9)
        printXY(lang[getLang("ui")]["strings"]["prompt_highscore_1"],0,gibbet["properties"]["lines"]+10)
        printXYraw("]>",0,gibbet["properties"]["lines"]+11)
        gameStats["userInput"]=input()
        if not(gameStats["userInput"] in {"",None}):
            addToHighscore(getLang("dict"),gameStats["userWord"],gameStats["userInput"],gameStats["userFails"]+gameStats["userTries"],gameTime,time.strftime(config["system"]["save-date-format-str"],time.localtime()),gameStats["guessedWord"],gameStats["state"],gameStats["userScore"])
def genList(lType):
    gList=[]
    gWord=""
    for j in lType:
        gList.append(lType[j]["properties"]["langID"])
        gWord+=lType[j]["properties"]["langID"]+lang[getLang("ui")]["strings"]["settings_for"]+lType[j]["properties"]["langName"]+"; "
    return {"gWord":gWord,"gList":gList}

def openOptions():
    global config
    oInput=""
    while not (oInput=="x"):
        clear()
        printXY(lang[getLang("ui")]["strings"]["settings_ui_lang"]+lang[config["user"]["lastUiLang"]]["properties"]["langName"]+" ("+config["user"]["lastUiLang"]+")",3,3)
        
        
        printXY(lang[getLang("ui")]["strings"]["settings_dict_lang"]+words[config["user"]["lastDictLang"]]["properties"]["langName"]+" ("+config["user"]["lastDictLang"]+")",3,4)
        
        
        printXY(lang[getLang("ui")]["strings"]["settings_show_word_on_loose"]+lang[getLang("ui")]["strings"][yn(config["user"]["show_word_on_loose"]).lower()],3,5)
        printXY(lang[getLang("ui")]["strings"]["settings_show_entered_letters"]+lang[getLang("ui")]["strings"][yn(config["user"]["show_entered_letters"]).lower()],3,6)
        printXY(lang[getLang("ui")]["strings"]["settings_start_with_random_letter"]+lang[getLang("ui")]["strings"][yn(config["user"]["start_with_random_letter"]).lower()],3,7)


        printXY(lang[getLang("ui")]["strings"]["settings_exit"],3,10)
        printXYraw("]>",0,12)
        
        
        oInput=input().lower().strip()
        if oInput=="3":
            config["user"]["show_word_on_loose"]=not(config["user"]["show_word_on_loose"])
        elif oInput=="4":
            config["user"]["show_entered_letters"]=not(config["user"]["show_entered_letters"])
        elif oInput=="5":
            config["user"]["start_with_random_letter"]=not(config["user"]["start_with_random_letter"])
        elif oInput=="1":
            ret=genList(lang)
            printXY(lang[getLang("ui")]["strings"]["settings_enter_valid"]+": "+(ret["gWord"].strip("; ")),0,14)
            lInput=""
            while not(lInput in ret["gList"]):
                printXYraw(" "*300,0,15)
                printXYraw("]>",0,15)
                lInput=input()
            config["user"]["lastUiLang"]=lInput
        elif oInput=="2":
            ret=genList(words)
            printXY(lang[getLang("ui")]["strings"]["settings_enter_valid"]+": "+(ret["gWord"].strip("; ")),0,14)
            lInput=""
            while not(lInput in ret["gList"]):
                printXYraw(" "*300,0,15)
                printXYraw("]>",0,15)
                lInput=input()
            config["user"]["lastDictLang"]=lInput
    saveConfig()

def showHighscore():
    global score
    tmp=""
    clear()
    for k in sorted(score):
        print("[ "+lang[k]["properties"]["langName"]+" ]")
        for l in sorted(score[k]):
            print(str(" "*2)+l)
            for m in sorted(score[k][l]):
                tmp=str(" "*5)+m+": "+lang[getLang("ui")]["strings"][score[k][l][m]["game_state"]+"_p"]
                tmp+="; "+str(score[k][l][m]["game_score"]).replace(".",lang[getLang("ui")]["strings"]["dec_sep"])+" "+lang[getLang("ui")]["strings"]["points"]
                tmp+="; "+time.strftime(lang[getLang("ui")]["properties"]["dateFormat"],(time.strptime(score[k][l][m]["date"],config["system"]["save-date-format-str"])))
                print(tmp)

    print("\n"*2+lang[getLang("ui")]["strings"]["score_reset"])
                
    if input()=="RESET":
        print(lang[getLang("ui")]["strings"]["score_reset_prompt"])
        if input().lower()[:1] in {"y","j",lang[getLang("ui")]["strings"]["yes"].lower()[:1]}:
            score.clear()
            saveScore()
def showHelp():
    clear()
    printXYraw("",0,0)
    printXY(lang[getLang("ui")]["strings"]["title"],9,2)
    printXY(lang[getLang("ui")]["strings"]["title_desc"],7,3)
    printXY(lang[getLang("ui")]["strings"]["game"]+": "+"© Copyright 2016 LukeSkywalk3r",7,4)
    printXY(lang[getLang("ui")]["strings"]["language"]+": "+lang[getLang("ui")]["rights"]["copyright"],7,5)
    printXY(lang[getLang("ui")]["strings"]["dict"]+": "+words[getLang("dict")]["rights"]["copyright"],7,6)
    printXYraw("",0,8)
    for line in lang[getLang("ui")]["strings"]["help_lines"]:
        print(line)
    printXY(lang[getLang("ui")]["strings"]["enter_to_continue"],0,len(lang[getLang("ui")]["strings"]["help_lines"])+9)
    
    input()
    
while True:
    mainMenu()

