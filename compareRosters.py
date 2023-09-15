from classes import Roster
import sys
import markdown2

def boldGreater(a, b):
    if(a > b):
        return "**" + str(a) + "**"
    else:
        return str(a)

def toMarkdown(roster1: Roster, roster2: Roster):
    markdownStr = ""
    markdownStr += "# Roster Analysis  \n"
    markdownStr += "Roster 1 Source: " + roster1.sourceFile + "  \n"
    markdownStr += "Roster 2 Source: " + roster2.sourceFile + "  \n"

    markdownStr += "| Group | R Total | R Avg | Y Total | Y Avg | A Total | A Avg | BCR | |"
    markdownStr += "| Group | R Total | R Avg | Y Total | Y Avg | A Total | A Avg | BCR |\n"
    markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"

    markdownStr += "| R1 O1" + roster1.offenseFirst.toMarkdown() + " | | R2 O1" + roster2.offenseFirst.toMarkdown() + " \n"
    markdownStr += "| R1 D1" + roster1.defenseFirst.toMarkdown() + " | | R2 D1" + roster2.defenseFirst.toMarkdown() + " \n"
    markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    markdownStr += "| R1 O2" + roster1.offenseSecond.toMarkdown() + " | | R2 O2" + roster2.offenseSecond.toMarkdown() + " \n"
    markdownStr += "| R1 D2" + roster1.defenseSecond.toMarkdown() + " | | R2 D2" + roster2.defenseSecond.toMarkdown() + " \n"
    markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    markdownStr += "| R1 1s" + roster1.firstStringStats.toMarkdown() + " | | R2 1s" + roster2.firstStringStats.toMarkdown() + " \n"
    markdownStr += "| R1 2s" + roster1.secondStringStats.toMarkdown() + " | | R2 2s" + roster2.secondStringStats.toMarkdown() + " \n"
    markdownStr += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    markdownStr += "| R1 T" + roster1.totalStats.toMarkdown() + " | | R2 T" + roster2.totalStats.toMarkdown() + " \n"
    return markdownStr

def toCsv(roster1: Roster, roster2: Roster):
    csv = ""
    csv += "Roster 1 Source: " + roster1.sourceFile + "\n"
    csv += "Roster 2 Source: " + roster2.sourceFile + "\n"
    csv += "R  | O/D | R Tot | R Avg | Y Tot | Y Avg | A Tot | A Avg | BCD |\n"



def compareRosters(roster1: Roster, roster2: Roster):
    roster1.calculateStatistics()
    roster2.calculateStatistics()

    print("Comparing rosters...")
    print("Roster 1: " + roster1.sourceFile)
    print("Roster 2: " + roster2.sourceFile)
    
    print("R  | O/D | R Tot | R Avg | Y Tot | Y Avg | A Tot | A Avg | BCD |")
    print("R1 |  O1 " + str(roster1.offenseFirst.toMarkdown()))
    print("R1 |  D1 " + str(roster1.defenseFirst.toMarkdown()))
    print("")
    print("R1 |  O2 " + str(roster1.offenseSecond.toMarkdown()))
    print("R1 |  D2 " + str(roster1.defenseSecond.toMarkdown()))
    print("")
    print("R1 |  1s " + str(roster1.firstStringStats.toMarkdown()))
    print("R1 |  2s " + str(roster1.secondStringStats.toMarkdown()))
    print("")
    print("R1 |  T " + str(roster1.totalStats.toMarkdown()))

    print("-" * 80)

    print("R  | O/D | R Tot | R Avg | Y Tot | Y Avg | A Tot | A Avg | BCD |")
    print("R2 |  O1 " + str(roster2.offenseFirst.toMarkdown()))
    print("R2 |  D1 " + str(roster2.defenseFirst.toMarkdown()))
    print("")
    print("R2 |  O2 " + str(roster2.offenseSecond.toMarkdown()))
    print("R2 |  D2 " + str(roster2.defenseSecond.toMarkdown()))
    print("")
    print("R2 |  1s " + str(roster2.firstStringStats.toMarkdown()))
    print("R2 |  2s " + str(roster2.secondStringStats.toMarkdown()))
    print("")
    print("R2 |  T " + str(roster2.totalStats.toMarkdown()))

    mdString = toMarkdown(roster1, roster2)

    with open("compare.md", 'w') as file:
        file.write(mdString)

    with open("compare.csv", 'w') as file:
        csv = ""
        csv = toMarkdown(roster1, roster2).replace("|", ",")
        file.write(csv)
        print(csv)

if __name__ == '__main__':
    # for element in sys.argv:
    #     print(element)

    if(len(sys.argv) < 2):
        print("usage: python compareRosters.py <roster1.csv> <roster2.csv>")
        print("No input file specified. Exiting...")


    print("Loading roster 1 from " + sys.argv[1])
    roster1 = Roster()
    file1 = open(sys.argv[1], 'rb')
    roster1.fromCsv(file1)
    roster1.sourceFile = sys.argv[1]
    file1.close()

    print("Loading roster 2 from " + sys.argv[2])
    roster2 = Roster()
    file2 = open(sys.argv[2], 'rb')
    roster2.fromCsv(file2)
    roster2.sourceFile = sys.argv[2]
    file2.close()

    print("*" * 80)
    print(roster1)
    print("*" * 80)
    print(roster2)
    print("*" * 80)

    compareRosters(roster1, roster2)
