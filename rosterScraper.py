# rosterScraper.py

import json
from classes import Player, Roster
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import sys
import markdown2

# url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/florida/90498"
# url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/tennessee/91993/"
# url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/kentucky/90866"
# url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/vanderbilt/92361"
# url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/south-carolina/91832"
url = "https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/georgia/90590"

url2 = "https://www.on3.com/db/search/?searchText="

ANNUAL_ADJUSTMENT_RATE = 0.02
CURRENT_YEAR = 2023

roster = Roster()

def getRequest(request):
    global counter
    counter = 0
    try:
        return urlopen(request)
    except Exception as e:
        print(e)
        # sleep for a bit in case that helps
        time.sleep(0.25)
        # try again
        counter += 1
        if counter > 5:
            raise Exception("Too many retries: " + str(request))
        else:
            return getRequest(request)

def testPlayerPosition(player, positionJson):
    # print("positionJson: " + positionJson + " | position: " + player.position)

    if(positionJson == "WR"):
        return (player.position == "WR-X" or
                player.position == "WR-Z" or
                player.position == "WR-Y" or
                player.position == "WR-F" or 
                player.position == "WR-SL" or
                player.position == "TE-F")

    if(positionJson == "IOL" or positionJson == "OT"):
        return (player.position == "RG" or
                player.position == "RT" or
                player.position == "LG" or
                player.position == "LT" or
                player.position == "OC")

    if(positionJson == "TE"):
        return (player.position == "TE" or 
                player.position == "TE/FB" or 
                player.position == "TE-H" or 
                player.position == "TE-F" or
                player.position == "RTE" or
                player.position == "LTE")
    
    if(positionJson == "RB"):
        return (player.position == "RB")
    
    if(positionJson == "QB"):
        return (player.position == "QB")
    
    # DEFENSE

    if(positionJson == "DL"):
        return (player.position == "DT" or
                player.position == "DE" or
                player.position == "NT" )
    
    if(positionJson == "LB"):
        return (player.position == "MLB" or
                player.position == "WLB" or
                player.position == "ANCHR" or
                player.position == "MAC" or
                player.position == "MONEY")
    
    if(positionJson == "CB" or positionJson == "S"):
        return (player.position == "LCB" or
                player.position == "RCB" or
                player.position == "BCB" or 
                player.position == "FCB" or 
                player.position == "FS" or
                player.position == "SS" or
                player.position == "STAR" or
                player.position == "ANCHR")
    
    if(positionJson == "EDGE"):
        return (player.position == "JACK" or
                player.position == "DE" or
                player.position == "DE" or
                player.position == "LEO"or
                player.position == "DT" or
                player.position == "DT" or
                player.position == "STAR")

    return False

def updatePlayer(player, elem):
    if( elem.get("division") == "NCAA-FB" and
        elem.get("classYear") > 2010):

        player.recruitingClass = elem["classYear"]

        if(elem.get("rating") and elem.get("rating").get("consensusRating")):
            rating_json = elem["rating"]
            player.rating = rating_json["consensusRating"]
            player.stars = rating_json["consensusStars"]
        return True

    else:
        # print("Update player " + player.firstName + " " + player.lastName + " failed")
        # print(json.dumps(elem, indent=4, sort_keys=True))
        return False

def findPlayer(player, elem_json):
    print("Searching for " + player.firstName + " " + player.lastName + "... ", end="")
    list = elem_json["props"]["pageProps"]["searchData"]["list"]

    jsonName = ""
    queryName = ""
    queryName2 = ""
    goesbyName = ""

    for elem in list:
        jsonName = ""
        queryName = ""
        queryName2 = ""
        goesbyName = ""

        if(elem.get("firstName") and elem.get("lastName")):
            jsonName = elem.get("firstName") + " " + elem.get("lastName")
            queryName = player.firstName + " " + player.lastName
            queryName2 = player.firstName + " " + player.lastName.split(" ")[0].strip()

        if(elem.get("goesBy")):
            goesbyName = elem.get("goesBy") + " " + elem.get("lastName")

        jsonName = jsonName.replace("'", "").replace(".", "")

        if(queryName.lower() == jsonName.lower() or
            queryName.lower() == goesbyName.lower() or
            queryName2.lower() == jsonName.lower() or
            queryName2.lower() == goesbyName.lower()):

            # print(elem.keys())
            # print(json.dumps(elem, indent=1, sort_keys=True))
            # print("pass name check")

            if(not elem.get("position")):
                print("position missing?")
                continue

            positionJson = elem.get("position").get("abbreviation")
            if(not testPlayerPosition(player, positionJson)):
                print("Pos Test Failed: " + player.position + " != " + positionJson )
                continue

            if(updatePlayer(player, elem)):
                print("FOUND")
                return True
        
        print("NOT FOUND")
        return False

def ballSide(position):
    if( 
        position == "WR-X" or
        position == "WR-Z" or
        position == "WR-Y" or
        position == "WR-SL" or
        position == "LT" or
        position == "LG" or
        position == "OC" or
        position == "RG" or
        position == "RT" or
        position == "TE" or
        position == "QB" or
        position == "RB"):
        return "offense"
    else:
        return "defense"

def makeName(player, playerText):
    output = playerText
    output = output.replace("/", "")
    output = output.replace("TR", "")
    output = output.replace("RS", "")
    output = output.replace("FR", "")
    output = output.replace("SO", "")
    output = output.replace("JR", "")
    output = output.replace("SR", "")
    output = output.replace("GR", "")

    names = output.split(",")
    print(names)
    player.firstName = names[1].strip()
    player.lastName = names[0].strip()
    return player

def populateRoster():
    print("Populating roster...")
    for player in roster.offenseFirst.players + roster.offenseSecond.players + roster.defenseFirst.players + roster.defenseSecond.players:
        if(player.rating == 0):
            searchUrl = player.searchUrl(url2)
            req = Request(searchUrl, headers={'User-Agent': 'Mozilla/5.0'})

            # print(searchUrl)

            page = getRequest(req)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")

            for elem in soup("script", id="__NEXT_DATA__"):
                elem_json = json.loads(elem.text)
                if(not findPlayer(player, elem_json)):
                    print(searchUrl)


def loadRoster():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = getRequest(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    roster.offenseFirst.players = []
    roster.offenseSecond.players = []
    roster.defenseFirst.players = []
    roster.defenseSecond.players = []

    # print(soup.get_text())
    rows_wht = soup("tr", class_="row-dc-wht")
    rows_grey = soup("tr", class_="row-dc-grey")

    for row in rows_wht + rows_grey:
        # print(row.text)

        # print(row.p["class"])
        # print(row['class'])
        position = row.find_next("td", class_=row['class'])
        player_1 = row.find_next("a")
        player_2 = player_1.find_next("a")

        if( position.text == "PT" or
            position.text == "PK" or
            position.text == "KO" or
            position.text == "LS" or
            position.text == "H" or
            position.text == "PR" or
            position.text == "KR" or
            position.text == "INJ" ):
            
            continue

        else:
            print(position.text + " | " + player_1.text + " | " + player_2.text)
            player1 = Player()
            player1.position = position.text
            player1.side = ballSide(position.text)
            player1 = makeName(player1, player_1.text)

            player2 = Player()
            if(len(player_2.text) > 0):
                player2.position = position.text
                player2.side = ballSide(position.text)
                player2 = makeName(player2, player_2.text)

            # print("Player 1: " + player1.firstName + " " + player1.lastName + " | " + player1.position + " | " + player1.side)
            # print("Player 2: " + player2.firstName + " " + player2.lastName + " | " + player2.position + " | " + player2.side)

            if(ballSide(position.text) == "offense"):
                roster.offenseFirst.players.append(player1)
                roster.offenseSecond.players.append(player2)
            else:
                roster.defenseFirst.players.append(player1)
                roster.defenseSecond.players.append(player2)

if __name__ == '__main__':

    roster = Roster()
    inputFilename = "roster.csv"
    inputFile = False

    # for element in sys.argv:
    #     print(element)

    if(len(sys.argv) > 1):
        inputFilename = sys.argv[1]
        inputFile = True
    
    rootFilename = inputFilename.replace(".csv", "")
    print("Input file: " + inputFilename)
    print("Root file: " + rootFilename)

    rosterLoaded = False

    try:
        file = open(inputFilename, 'rb')
        # roster = pickle.load(file)
        roster.fromCsv(file)
        file.close()
        rosterLoaded = True

    except FileNotFoundError:
        if(len(sys.argv) > 2):
            print("Roster file (" + inputFilename + ") not found. Exiting...")
            exit()
        else:
            print("No roster file found. Creating new file")

    print("Roster loaded: " + str(rosterLoaded))

    if(not rosterLoaded):
        roster = Roster()
        loadRoster()

    populateRoster()
    roster.calculateStatistics()
        
    print("First String Offense")
    print(roster.offenseFirst)

    print("\nFirst String Defense")
    print(roster.defenseFirst)

    print("\nSecond String Offense")
    print(roster.offenseSecond)

    print("\nSecond String Defense")
    print(roster.defenseSecond)

    print("\nStarters")
    print(roster.firstStringStats)

    print("\n2nd String")
    print(roster.secondStringStats)

    print("\nTotal")
    print(roster.totalStats)

    mdString = roster.toMarkdown(rootFilename, url)

    filename = rootFilename + ".md"
    with open(rootFilename + ".md", 'w') as file:
        print("Writing MD to " + filename)
        file.write(mdString)

    csv = roster.toCsv()
    filename = rootFilename + ".csv"
    with open(filename, 'w') as file:
        print("Writing CSV to " + filename)
        file.write(csv)


