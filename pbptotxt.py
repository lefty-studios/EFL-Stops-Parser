import urllib.request as urllib2
import html2text
import requests
from bs4 import BeautifulSoup
import csv

playersArrTotal = [""]
stopsArrTotal = [0]  
passStopsArrTotal = [0]  
rushStopsArrTotal = [0]  

def getPbps(start, end, season):
    playersArr = [""]
    stopsArr = [0]  
    passStopsArr = [0]  
    rushStopsArr = [0]  
    def addStops(nameP, l):
        if nameP == "None":
            print(l)
        if nameP in playersArr:
            #print(nameP)
            stopsArr[playersArr.index(playerName)]+=1
            #print(nameP + "'s current stops are " + str(stopsArr[playersArr.index(playerName)]))
        else:
            #print(nameP + " does not exist yet")
            stopsArr.append(1)
            playersArr.append(playerName)
        if nameP in playersArrTotal:
            #print(nameP)
            stopsArrTotal[playersArrTotal.index(playerName)]+=1
            #print(nameP + "'s current stops are " + str(stopsArr[playersArr.index(playerName)]))
        else:
            #print(nameP + " does not exist yet")
            stopsArrTotal.append(1)
            playersArrTotal.append(playerName)

    i = start
    while i <= end:
        if "28" not in season:
            url="https://efl.network/index/efl-history/"+season+"/Logs/"+str(i)+".html"
        else: 
            url="https://efl.network/index/efl/Logs/"+str(i)+".html"
        html = requests.get(url)
        
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 1000
        newData = h.handle(html.text)
        newData = newData.replace("| ", ".")
        newData = newData.replace("| ", ".")
        newData = newData.replace("\---", "")
        newData = newData.replace("for a short gain.", "for 0 yds.")
        newData = newData.replace("2 Dope", "2-Dope")
        newData = newData.replace("Jr.", "Jr")
        
        f = open("C:\EFL\EFL\pbp_" +season+"_efl_" +str(i)+".txt", "w")
        f.write(newData)
        f.close()
        file1 = open("C:\EFL\EFL\pbp_" +season+"_efl_" +str(i)+".txt", "r")
        count = 0

        print("C:\EFL\EFL\pbp_" +season+"_efl_" +str(i)+".txt")  

        while True:
            count += 1
        
            # Get next line from file
            line = file1.readline()
            split = line.split(".")

            resultLong = None
            playerNameLong = None
            playerName = "None"

            if "INTERCEPTION" in line:
                
                playerNameLong = split[7].split(" ")
                #print(playerNameLong)
                if len(playerNameLong) > 4:
                    playerName = playerNameLong[3] + " " + playerNameLong[4] 
                else: 
                    playerName = playerNameLong[3] 
                #print(playerName)
                addStops(playerName, line)
            if "SACKED" in line and ("3rd" or "4th") in line:
                    
                    playerNameLong = split[5].split(" ")
                    #print(playerNameLong)
                    #print(playerNameLong[3])
                    if len(playerNameLong) > 4:
                        playerName = playerNameLong[4] + ", " +playerNameLong[3][0]
                    #print(playerName)
                    addStops(playerName, line)
            if ("3rd" or "4th") in line and "Tackle by" in line and "TOUCHDOWN" not in line and "Timeout" not in line and "Penalty" not in line and "Punt" not in line:
                #print(line)
                
                downAndDistance = split[2].split(" ")
                if "Goal" not in line:
                    distance = int(downAndDistance[2])
                else:
                    distance = 10

                pN = split[4].split(" ")
                offensivePlayerName = pN[2] + " " + pN[3] 
                ##print(playerName)

                
                if "Rush" in line and "gain" not in line and "Fumble" not in line:
                    #print(split)
                    resultLong = split[5].split(" ")
                    #print(resultLong)
                    #print(i)
                    result = resultLong[2]
                    

                    playerNameLong = split[6].split(" ")
                    if len(playerNameLong) > 4:
                        playerName = playerNameLong[3] + " " + playerNameLong[4] 
                    else: 
                        playerName = playerNameLong[3] 
                    #print(playerName)
                if "gain" in line:
                    result = 0
                if "Pass" in line and "incomplete" not in line and "dropped" not in line and "INTERCEPTION" not in line and "SACKED" not in line:
                    #print(split)
                    resultLong = split[6].split(" ")
                    result = resultLong[2]
                    #print("result " + result)
                    if "a" in str(result):
                        print(resultLong)
                    ##print("result " + result)

                    playerNameLong = split[7].split(" ")
                    #print(playerNameLong)
                    if len(playerNameLong) > 4:
                        playerName = playerNameLong[3] + " " + playerNameLong[4] 
                    else: 
                        playerName = playerNameLong[3] 
                    ##print(playerName)
                
                if int(result) < int(distance):
                    #stops stuff
                    #print(line)
                    addStops(playerName, line)

                        # if line is empty
            # end of file is reached
            if not line:
                break

        
        i += 1

    #for x in range(1, len(playersArr)):
        #print(str(playersArr[x]) + " " + str(stopsArr[x]))

    #print(playersArr)

    with open("C:/EFL/" + season + "_stops_data.csv", 'w', newline='') as csvfile:
        fieldnames = ['player_name', 'stops']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for x in range(1, len(playersArr)):
            writer.writerow({'player_name': str(playersArr[x]), 'stops': str(stopsArr[x])})
        

getPbps(207,302,"S021")
getPbps(207,302,"S022")
getPbps(111,206,"S023")
getPbps(111,206,"S024")
getPbps(111,206,"S025")
getPbps(207,302,"S026")
getPbps(111,206,"S027")
getPbps(303,398,"S028")

with open("C:/EFL/alltime_stops_data.csv", 'w', newline='') as csvfile:
    fieldnames = ['player_name', 'stops']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for x in range(1, len(playersArrTotal)):
        writer.writerow({'player_name': str(playersArrTotal[x]), 'stops': str(stopsArrTotal[x])})
