#import modules
import requests #Handles API requests
import time 
import pandas as pd 

#setup API URLS and key
summonerData = "https://na1.api.riotgames.com/lol/summoner/v4/summoners"
matchList = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account"
matchData = "https://na1.api.riotgames.com/lol/match/v4/matches"
key = [ENTER OWN KEY]

#API CALLS seperated into different functions
def Request(name): #Gets the Summoner Data
    time.sleep(1)
    print("Connecting to Riots API....")
    URL = "{}/by-name/{}?api_key={}".format(summonerData,name,key)
    response = requests.get(URL)
    return response.json()

def MatchList(accountId): #Creates a list of the 100 games match ids
        time.sleep(1)
        matchesList = []
        URL = "{}/{}?api_key={}".format(matchList, accountId ,key)
        response = requests.get(URL)
        print('Getting match list....')
        matches = response.json()
        for i in range(len(matches['matches'])):
            matchesList.append(str(matches['matches'][i]['gameId']))
        return matchesList

def reqMatch(matchId): #Get match data by a matchId
    time.sleep(1)
    URL = "{}/{}?api_key={}".format(matchData, matchId ,key)
    response = requests.get(URL)
    return response.json()

#Main Function
def main():

    #Get user input, TODO: Make it so if you enter any bad username it would say to enter a valid username and repeat
    name = input('Name: ')
    data = Request(name)
    accountId = data['accountId']
    ListofMatches = MatchList(accountId)

    #Create an empty dictonary for JSON Data we want to store
    jd = {} 

    print('Creating the dataframe....(this will take a few momments)') #Takes a while because of each call we make to the Match API. 

    #Iterate through the match id list
    for matchNum in range(len(ListofMatches)):
        matchData = reqMatch(ListofMatches[matchNum])

        #Iterate through to find the correct Participant Id
        for summonerId in range(len(matchData['participantIdentities'])):
            if matchData['participantIdentities'][summonerId]['player']['summonerName'].lower() == name.lower(): #checks if the two match,  using lower so if they entered uppercase it works
                participantId = summonerId   

        #Create a nested dictonary where each game is saved into a dictonary TODO Figure out how to get CS Diff @ 10 and CS @ 10, can get but if its a Remake throws an Key Error 
        jd.update( {'Game ' + str(matchNum) : { 'kills' : matchData['participants'][participantId]['stats']['kills'],
                                        'Deaths' : matchData['participants'][participantId]['stats']['deaths'],
                                        'Assists' : matchData['participants'][participantId]['stats']['assists'], 
                                        'Win' :  matchData['participants'][participantId]['stats']['win'],
                                        'Gold Earn' : matchData['participants'][participantId]['stats']['goldEarned'],
                                        'Gold Spent' : matchData['participants'][participantId]['stats']['goldSpent'],
                                        'Total Damage Dealt to Champions' : matchData['participants'][participantId]['stats']['totalDamageDealtToChampions'],
                                        'Total Damage Taken' : matchData['participants'][participantId]['stats']['totalDamageTaken'],
                                        'Vision Score' : matchData['participants'][participantId]['stats']['visionScore'],
                                        'Wards Placed' : matchData['participants'][participantId]['stats']['wardsPlaced'],
                                        'Wards Killed' : matchData['participants'][participantId]['stats']['visionScore'],
                                        'Vision Wards Bought': matchData['participants'][participantId]['stats']['visionWardsBoughtInGame'],
                                        'Total Minions Killed' : matchData['participants'][participantId]['stats']['totalMinionsKilled'],
                                        'Netural Monsters' : matchData['participants'][participantId]['stats']['neutralMinionsKilled']
            }} )

    #Create the Pandas Dataframe
    df = pd.DataFrame.from_dict(jd, orient='index')
    print('Dataframe built, exporting to CSV')
    df.to_csv('data.csv')
    print('CSV created!, exiting')
 
if __name__ == '__main__':
    main()



