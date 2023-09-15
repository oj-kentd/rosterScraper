ANNUAL_ADJUSTMENT_RATE = 0.02
CURRENT_YEAR = 2023

class Stats:
    recruitingTotal = 0.0
    recruitingAvg = 0.0
    adjustedTotal = 0.0
    adjustedAvg = 0.0
    yearsTotal = 0.0
    yearsAvg = 0.0
    blueChipRatio = 0.0

    def toCsv(self):
        csvStr = ""
        csvStr += str(f"{self.recruitingTotal:.2f}") + ","
        csvStr += str(f"{self.recruitingAvg:.2f}") + ","
        csvStr += str(self.yearsTotal) + ","
        csvStr += str(f"{self.yearsAvg:.2f}") + ","
        csvStr += str(f"{self.adjustedTotal:.2f}") + ","
        csvStr += str(f"{self.adjustedAvg:.2f}") + ","
        csvStr += str(f"{self.blueChipRatio:.2f}")
        return csvStr
      

    def toMarkdown(self):
        markdownStr = ""
        markdownStr += " | " + str(f"{self.recruitingTotal:.2f}")
        markdownStr += " | " + str(f"{self.recruitingAvg:.2f}")
        markdownStr += " | " + str(self.yearsTotal)
        markdownStr += " | " + str(f"{self.yearsAvg:.2f}")
        markdownStr += " | " + str(f"{self.adjustedTotal:.2f}")
        markdownStr += " | " + str(f"{self.adjustedAvg:.2f}")
        markdownStr += " | " + str(f"{self.blueChipRatio:.2f}")
        markdownStr += " | "
        return markdownStr

    def __repr__(self):
        output = ""
        output += "-" * 100 + "\n"
        output += "\tRecruiting | " + str(f"{self.recruitingTotal:.2f}") + "\t| " + str(f"{self.recruitingAvg:.2f}") + "\n"
        output += "\tYears      | " + str(self.yearsTotal) + "\t\t| " + str(f"{self.yearsAvg:.2f}") + "\n"
        output += "\tAdjusted   | " + str(f"{self.adjustedTotal:.2f}") + "\t| " + str(f"{self.adjustedAvg:.2f}") + "\n"
        output += "\tBCR        | " + str(f"{self.blueChipRatio:.2f}") + "\n"
        output += "-" * 100 + "\n"
        return output

class Grouping:
    players = []
    stats = Stats()

    def calcStatistics(self):
        self.stats = Stats()
        self.stats.recruitingTotal = 0
        self.stats.recruitingAvg = 0
        self.stats.adjustedTotal = 0
        self.stats.adjustedAvg = 0
        self.stats.yearsTotal = 0
        self.stats.yearsAvg = 0
        self.stats.blueChipRatio = 0

        ratings = []
        years = []
        adjusted = []
        blueChips = 0

        for player in self.players:
            if(player.rating > 0): # If the player has a rating
                playerYears = CURRENT_YEAR - player.recruitingClass
                years.append(playerYears)
                ratings.append(player.rating)
                adjustmentFactor = 1 + (ANNUAL_ADJUSTMENT_RATE * playerYears)
                adjusted.append(player.rating * adjustmentFactor)
            
            if(player.stars >= 4):
                blueChips += 1
    
        self.stats.recruitingTotal = sum(ratings)
        self.stats.recruitingAvg = self.stats.recruitingTotal / len(ratings)
        
        self.stats.yearsTotal = sum(years)
        self.stats.yearsAvg = self.stats.yearsTotal / len(years)

        self.stats.adjustedTotal = sum(adjusted)
        self.stats.adjustedAvg = self.stats.adjustedTotal / len(adjusted)

        self.stats.blueChipRatio = (blueChips / len(self.players)) * 100.0

    def toMarkdown(self):
        return self.stats.toMarkdown()

    def __repr__(self):
        output = str(self.stats)
        return output

class Player:
    position = ""
    side = ""
    firstName = ""
    lastName = ""
    rating = 0.0
    stars = 0
    recruitingClass = 0
    
    def searchUrl(self, url):
        self.firstName = self.firstName.replace("'", "").replace(".", "").strip()
        self.lastName = self.lastName.replace("'", "").replace(".", "").strip()

        searchString = str(self.firstName + "%20" + self.lastName.replace(" ", "%20"))
        return (url + searchString)

    def __repr__(self):
        return self.firstName + " " + self.lastName + " | " + self.position + " | " + str(f"{self.rating:.2f}") + " | " + str(self.stars) + " | " + str(self.recruitingClass)
    
    def toMarkdown(self):
        return "|" + self.firstName + " " + self.lastName + " | " + self.position + " | " + str(f"{self.rating:.2f}") + " | " + str(self.stars) + " | " + str(self.recruitingClass)
        
class Roster:
    offenseFirst = Grouping()
    offenseSecond = Grouping()
    defenseFirst = Grouping()
    defenseSecond = Grouping()

    firstStringStats = Stats()
    secondStringStats = Stats()
    totalStats = Stats()
    sourceFile = ""

    def __init__(self):
        self.offenseFirst = Grouping()
        self.offenseSecond = Grouping()
        self.defenseFirst = Grouping()
        self.defenseSecond = Grouping()

        self.firstStringStats = Stats()
        self.secondStringStats = Stats()
        self.totalStats = Stats()
        self.sourceFile = ""

    def calculateStatistics(self):
        self.firstStringStats = Stats()
        self.secondStringStats = Stats()
        self.totalStats = Stats()

        self.offenseFirst.calcStatistics()
        self.offenseSecond.calcStatistics()
        self.defenseFirst.calcStatistics()
        self.defenseSecond.calcStatistics()

        # print(len(self.offenseFirst.players))
        # print(len(self.defenseFirst.players))
        # print(len(self.offenseSecond.players))
        # print(len(self.defenseSecond.players))

        # print(self.offenseFirst)
        # print(self.offenseSecond)
        # print(self.defenseFirst)
        # print(self.defenseSecond)

        self.firstStringStats.recruitingTotal = self.offenseFirst.stats.recruitingTotal + self.defenseFirst.stats.recruitingTotal
        self.firstStringStats.recruitingAvg = (self.offenseFirst.stats.recruitingAvg + self.defenseFirst.stats.recruitingAvg) / 2.0
        self.firstStringStats.yearsTotal = self.offenseFirst.stats.yearsTotal + self.defenseFirst.stats.yearsTotal
        self.firstStringStats.yearsAvg = (self.offenseFirst.stats.yearsAvg + self.defenseFirst.stats.yearsAvg) / 2.0
        self.firstStringStats.adjustedTotal = self.offenseFirst.stats.adjustedTotal + self.defenseFirst.stats.adjustedTotal
        self.firstStringStats.adjustedAvg = (self.offenseFirst.stats.adjustedAvg + self.defenseFirst.stats.adjustedAvg) / 2.0
        self.firstStringStats.blueChipRatio = (self.offenseFirst.stats.blueChipRatio + self.defenseFirst.stats.blueChipRatio) / 2.0

        self.secondStringStats.recruitingTotal = self.offenseSecond.stats.recruitingTotal + self.defenseSecond.stats.recruitingTotal
        self.secondStringStats.recruitingAvg = (self.offenseSecond.stats.recruitingAvg + self.defenseSecond.stats.recruitingAvg) / 2.0
        self.secondStringStats.yearsTotal = self.offenseSecond.stats.yearsTotal + self.defenseSecond.stats.yearsTotal
        self.secondStringStats.yearsAvg = (self.offenseSecond.stats.yearsAvg + self.defenseSecond.stats.yearsAvg) / 2.0
        self.secondStringStats.adjustedTotal = self.offenseSecond.stats.adjustedTotal + self.defenseSecond.stats.adjustedTotal
        self.secondStringStats.adjustedAvg = (self.offenseSecond.stats.adjustedAvg + self.defenseSecond.stats.adjustedAvg) / 2.0
        self.secondStringStats.blueChipRatio = (self.offenseSecond.stats.blueChipRatio + self.defenseSecond.stats.blueChipRatio) / 2.0

        self.totalStats.recruitingTotal = self.offenseFirst.stats.recruitingTotal + self.defenseFirst.stats.recruitingTotal + self.offenseSecond.stats.recruitingTotal + self.defenseSecond.stats.recruitingTotal
        self.totalStats.recruitingAvg = (self.offenseFirst.stats.recruitingAvg + self.defenseFirst.stats.recruitingAvg + self.offenseSecond.stats.recruitingAvg + self.defenseSecond.stats.recruitingAvg) / 4.0
        self.totalStats.yearsTotal = self.offenseFirst.stats.yearsTotal + self.defenseFirst.stats.yearsTotal + self.offenseSecond.stats.yearsTotal + self.defenseSecond.stats.yearsTotal
        self.totalStats.yearsAvg = (self.offenseFirst.stats.yearsAvg + self.defenseFirst.stats.yearsAvg + self.offenseSecond.stats.yearsAvg + self.defenseSecond.stats.yearsAvg) / 4.0
        self.totalStats.adjustedTotal = self.offenseFirst.stats.adjustedTotal + self.defenseFirst.stats.adjustedTotal + self.offenseSecond.stats.adjustedTotal + self.defenseSecond.stats.adjustedTotal
        self.totalStats.adjustedAvg = (self.offenseFirst.stats.adjustedAvg + self.defenseFirst.stats.adjustedAvg + self.offenseSecond.stats.adjustedAvg + self.defenseSecond.stats.adjustedAvg) / 4.0
        self.totalStats.blueChipRatio = (self.offenseFirst.stats.blueChipRatio + self.defenseFirst.stats.blueChipRatio + self.offenseSecond.stats.blueChipRatio + self.defenseSecond.stats.blueChipRatio) / 4.0

    def toCsv(self):
        csv = ""
        for player in self.offenseFirst.players:
            csv += "O,1," + player.firstName + "," + player.lastName + "," + player.position + "," + player.side + "," + str(player.rating) + "," + str(player.stars) + "," + str(player.recruitingClass) + "\n"

        for player in self.offenseSecond.players:
            csv += "O,2," + player.firstName + "," + player.lastName + "," + player.position + "," + player.side + "," + str(player.rating) + "," + str(player.stars) + "," + str(player.recruitingClass) + "\n"

        for player in self.defenseFirst.players:
            csv += "D,1," + player.firstName + "," + player.lastName + "," + player.position + "," + player.side + "," + str(player.rating) + "," + str(player.stars) + "," + str(player.recruitingClass) + "\n"

        for player in self.defenseSecond.players:
            csv += "D,2," + player.firstName + "," + player.lastName + "," + player.position + "," + player.side + "," + str(player.rating) + "," + str(player.stars) + "," + str(player.recruitingClass) + "\n"

        csv += "\n"
        csv += "Group, Recruiting Total, Recruiting Avg, Years Total. Years Avg. Adjusted Total, Adjusted Avg, BCR\n"
        csv += "Offense 1," + self.offenseFirst.stats.toCsv() + "\n"
        csv += "Defense 1," + self.defenseFirst.stats.toCsv() + "\n"
        csv += "\n"
        csv += "Offense 2," + self.offenseSecond.stats.toCsv() + "\n"
        csv += "Defense 2," + self.defenseSecond.stats.toCsv() + "\n"
        csv += "\n"
        csv += "1s," + self.firstStringStats.toCsv() + "\n"
        csv += "2s," + self.secondStringStats.toCsv() + "\n"
        csv += "\n"
        csv += "Total," + self.totalStats.toCsv() + "\n"

        return csv

    def fromCsv(self, file):
        self.offenseFirst.players = []
        self.offenseSecond.players = []
        self.defenseFirst.players = []
        self.defenseSecond.players = []

        for line in file:
            line = line.decode("utf-8")

            if (len(line.strip())) == 0 or (len(line.replace(",", "").strip())) == 0:
                print(line)
                # Blank Line: End of input data
                break

            tokens = line.split(",")

            # print(line)
            # print(tokens)
            # print(len(tokens))

            length = len(line.replace(",", "").strip())

            print(length)

            if(len(tokens) == 0):
                print(line)
                continue
            
            # print(tokens[0])
            if(not (tokens[0] == "O" or tokens[0] == "D")):
                print(line)
                continue

            # Results
            side = tokens[0]
            depth = int(tokens[1])
            player = Player()
            player.firstName = tokens[2]
            player.lastName = tokens[3]
            player.position = tokens[4]
            player.side = tokens[5]
            player.rating = float(tokens[6])
            player.stars = int(tokens[7])
            player.recruitingClass = int(tokens[8])

            # print(player)
            # print("Side: " + side + " Depth: " + str(depth))

            if(side == "O" and depth == 1):
                print("Adding "+ player.firstName + " " + player.lastName + " to O1")
                self.offenseFirst.players.append(player)
            
            elif (side == "O" and depth == 2):
                print("Adding "+ player.firstName + " " + player.lastName + " to O2")
                self.offenseSecond.players.append(player)
            
            elif (side == "D" and depth == 1):
                print("Adding "+ player.firstName + " " + player.lastName + " to D1")
                self.defenseFirst.players.append(player)
            
            elif (side == "D" and depth == 2):
                print("Adding "+ player.firstName + " " + player.lastName + " to D2")
                self.defenseSecond.players.append(player)

        # self.calculateStatistics()

    def __repr__(self):
        output = ""
        output += "-" * 100 + "\n"
        output += "--- Offense First String " + str(len(self.offenseFirst.players)) + " ----\n"
        for player in self.offenseFirst.players:
            output += "\t" + str(player) + "\n"

        output += "---- Offense Second String " + str(len(self.offenseSecond.players)) + " ----\n"
        for player in self.offenseSecond.players:
            output += "\t" + str(player) + "\n"

        output += "---- Defense First String " + str(len(self.defenseFirst.players)) + " ----\n"
        for player in self.defenseFirst.players:
            output += "\t" + str(player) + "\n"

        output += "---- Defense Second String " + str(len(self.defenseSecond.players)) + " ----\n"
        for player in self.defenseSecond.players:
            output += "\t" + str(player) + "\n"

        return output
    
    def toMarkdown(self, filename, url):
        markdownStr = ""
        markdownStr += "# Roster Analysis\n"
        markdownStr += "Source: " + url + "\n"

        markdownStr += "\n"
        markdownStr += "## Offense\n"
        markdownStr += "**First String**\n"
        markdownStr += "| Name | Position | Rating | Stars | Recruiting Class |\n"
        markdownStr += "| --- | --- | --- | --- | --- |\n"
        for player in self.offenseFirst.players:
            markdownStr += player.toMarkdown() + "\n"

        markdownStr += "\n"
        markdownStr += "**Second String**\n"
        markdownStr += "| Name | Position | Rating | Stars | Recruiting Class |\n"
        markdownStr += "| --- | --- | --- | --- | --- |\n"
        for player in self.offenseSecond.players:
            markdownStr += player.toMarkdown() + "\n"

        markdownStr += "\n"
        markdownStr += "## Defense\n"
        markdownStr += "**First String**\n"
        markdownStr += "| Name | Position | Rating | Stars | Recruiting Class |\n"
        markdownStr += "| --- | --- | --- | --- | --- |\n"
        for player in self.defenseFirst.players:
            markdownStr += player.toMarkdown() + "\n"
        
        markdownStr += "\n"

        markdownStr += "**Second String**\n"
        markdownStr += "| Name | Position | Rating | Stars | Recruiting Class |\n"
        markdownStr += "| --- | --- | --- | --- | --- |\n"
        for player in self.defenseSecond.players:
            markdownStr += player.toMarkdown() + "\n"

        markdownStr += "## Statistics\n"

        # markdownStr += "## Summary\n"
        markdownStr += "| Group | Recruiting Total | Recruiting Avg | Years Total | Years Avg | Adjusted Total | Adjusted Avg | BCR |\n"
        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        markdownStr += "| Offense 1" + self.offenseFirst.toMarkdown() + "\n"
        markdownStr += "| Defense 1 " + self.defenseFirst.toMarkdown() + " \n"
        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        markdownStr += "| Offense 2 " + self.offenseSecond.toMarkdown() + " \n"
        markdownStr += "| Defense 2 " + self.defenseSecond.toMarkdown() + " \n"
        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"

        markdownStr += "| Starters | " + str(f"{self.firstStringStats.recruitingTotal:.2f}")
        markdownStr += "| " + str(f"{self.firstStringStats.recruitingAvg:.2f}")
        markdownStr += "| " + str(self.firstStringStats.yearsTotal)
        markdownStr += "| " + str(f"{self.firstStringStats.yearsAvg:.2f}")
        markdownStr += "| " + str(f"{self.firstStringStats.adjustedTotal:.2f}")
        markdownStr += "| " + str(f"{self.firstStringStats.adjustedAvg:.2f}")
        markdownStr += "| " + str(f"{self.firstStringStats.blueChipRatio:.2f}")

        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"

        markdownStr += "| 2nd | " + str(f"{self.secondStringStats.recruitingTotal:.2f}")
        markdownStr += "| " + str(f"{self.secondStringStats.recruitingAvg:.2f}")
        markdownStr += "| " + str(self.secondStringStats.yearsTotal)
        markdownStr += "| " + str(f"{self.secondStringStats.yearsAvg:.2f}")
        markdownStr += "| " + str(f"{self.secondStringStats.adjustedTotal:.2f}")
        markdownStr += "| " + str(f"{self.secondStringStats.adjustedAvg:.2f}")
        markdownStr += "| " + str(f"{self.secondStringStats.blueChipRatio:.2f}")

        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        markdownStr += "| Total | " + str(f"{self.totalStats.recruitingTotal:.2f}")
        markdownStr += "| " + str(f"{self.totalStats.recruitingAvg:.2f}")
        markdownStr += "| " + str(self.totalStats.yearsTotal)
        markdownStr += "| " + str(f"{self.totalStats.yearsAvg:.2f}")
        markdownStr += "| " + str(f"{self.totalStats.adjustedTotal:.2f}")
        markdownStr += "| " + str(f"{self.totalStats.adjustedAvg:.2f}")
        markdownStr += "| " + str(f"{self.totalStats.blueChipRatio:.2f}")
        markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"

        return markdownStr