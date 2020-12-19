# RecNet Event Searcher by Jegarde
# I hope you like my spaghetti code lol

import requests
import time

def Initialize():
    global flaggedEventCount
    global flaggedWords
    global eventAmount
    global eventsSearched
    flaggedEventCount = 0
    flaggedWords = []
    eventAmount = 0
    eventsSearched = 0

def StartProcess(outputMode, flaggedWords, eventAmount):
    eventsApi = requests.get("https://api.rec.net/api/playerevents/v1?take="+str(eventAmount))
    print("Connection to API = "+str(eventsApi.ok))
    eventsApiJson = eventsApi.json()

    i = 0
    for x in eventsApiJson:
        accountApi = requests.get("https://accounts.rec.net/account/" + str(eventsApiJson[i]["CreatorPlayerId"]))
        accountApiJson = accountApi.json()

        event = [accountApiJson["displayName"], eventsApiJson[i]["Name"], eventsApiJson[i]["Description"]]

        checkFlaggedinName = [ele for ele in flaggedWords if (ele in str(event[1].casefold()))]
        checkFlaggedinDescription = [ele for ele in flaggedWords if (ele in str(event[2]).casefold())]

        if bool(checkFlaggedinName) or bool(checkFlaggedinDescription):
            print("https://rec.net/event/"+str(eventsApiJson[i]["PlayerEventId"])+"\nUsername: " + str(event[0]) + "\nEvent Name: " + str(event[1]) + "\nEvent Description: "+ str(event[2]) + "\n")
            global flaggedEventCount
            flaggedEventCount += 1

        i += 1
        global eventsSearched
        eventsSearched = i

def PrintConclusion(flaggedWords, flaggedEventCount, eventsSearched, timeElapsed):
    global extraTime
    print("---------------------------------------------------\nCONCLUSION\nFlagged Words: " + str(flaggedWords) + "\nFlagged Events Count: " + str(flaggedEventCount)+"\nEvents searched in total: " + str(eventsSearched)+"\nTime elapsed: "+str(round(timeElapsed-extraTime))+" seconds")

def InputWordsToSearch():
    input_string = input("Input words to search separated by space: ")
    global flaggedWords
    flaggedWords = input_string.split()
    print("Searching for the following words: " + str(flaggedWords)+"\n")

def InputAmountToSearch():
    global eventAmount
    eventAmount = input("Input many events should be searched: ")
    print("Searching " + str(eventAmount)+" events.\n")

Initialize()
InputWordsToSearch()
InputAmountToSearch()

extraTime = time.perf_counter()
StartProcess("1", flaggedWords, eventAmount)
PrintConclusion(flaggedWords, flaggedEventCount, eventsSearched, time.perf_counter())
