# bot.py
import os
import csv
import random
from Database import *
from cricketWriteups import *
from keep_alive import keep_alive
import discord
from dotenv import load_dotenv
import sqlite3
print("HI")
makeTables()
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
print(len(Database))
conn.commit()


def sum_list(items):
    sum_numbers = 0
    for x in items:
        sum_numbers += x
    return sum_numbers
class Game(object):
    def __init__(self, channelId,team1,team2, player1Id,player2Id,gameId):
      self.channelId= channelId
      self.player1 = player1Id
      self.player2 = player2Id
      self.gameId = gameId
      self.runs = 0
      self.bowlerNumber = 0
      self.userTurn = 0
      self.currentInningWickets = 0
      self.inning1Score = 0
      self.inning1Result = ""
      self.inning2Score = " "
      self.balls = 0
      self.innings = 1
      self.gameHappening = True 
      self.coinToss = True
      self.tossDecision = True
      self.team1 = team1
      self.team2 = team2
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
games = []
userTurn = 0
bowlerNumber = 0
wickets = 0
gameStarted = False

def convertBoolToInt(value):
    if(value == True):
        return 1
    else:
        return 0
def convertIntToBool(value):
    if(int(value)==1):
        print(value)
        print("T")
        return True
    else:
        return False
def sendGameValues(games):
    print("GOT HERE")
    conn = sqlite3.connect('users.db', timeout=1)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM games;',)
    dataDump = []
    for n in range(len(games)):
        specificGame = games[n]
     
        print(len(games))
       
        gameHappening = convertBoolToInt(specificGame.gameHappening)
        coinToss = convertBoolToInt(specificGame.coinToss)
        tossDecision = convertBoolToInt(specificGame.tossDecision)
        cursor.execute("insert into games (channelId, player1, player2, gameId, runs, bowlerNumber, userTurn, currentInningsWickets, inning1Score, inning1Result, balls, innings, gameHappening, coinToss, tossDecision, team1, team2) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(specificGame.channelId, specificGame.player1, specificGame.player2,specificGame.gameId, specificGame.runs,specificGame.bowlerNumber,specificGame.userTurn, specificGame.currentInningWickets,specificGame.inning1Score, specificGame.inning1Result, specificGame.balls, specificGame.innings,gameHappening,coinToss,tossDecision, specificGame.team1, specificGame.team2))
        dump = [specificGame.channelId, specificGame.player1, specificGame.player2,specificGame.gameId, specificGame.runs,specificGame.bowlerNumber,specificGame.userTurn, specificGame.currentInningWickets,specificGame.inning1Score, specificGame.inning1Result, specificGame.balls, specificGame.innings,gameHappening,coinToss,tossDecision, specificGame.team1, specificGame.team2]
        dataDump.append(dump)

        conn.commit()
    filename = "games.csv"
    
# writing to csv file  
    with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
      csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
        
        
    # writing the data rows  
      csvwriter.writerows(dataDump) 
    conn.commit()
    conn.close()
  
def importGameValues():
    conn = sqlite3.connect('users.db', timeout=1)
    cursor = conn.cursor()
    gameData = cursor.execute("SELECT channelId, player1, player2, gameId, runs, bowlerNumber, userTurn, currentInningsWickets, inning1Score, inning1Result, balls, innings, gameHappening, coinToss, tossDecision, team1, team2 FROM games").fetchall()
    print(gameData)
    games = []
    for n in range(len(gameData)):
        currentGame = gameData[n]
        dump = Game(currentGame[0],currentGame[15],currentGame[16],currentGame[1],currentGame[2],currentGame[3])
        dump.runs = currentGame[4]
        dump.bowlerNumber = currentGame[5]        
        dump.userTurn = currentGame[6]
        dump.currentInningWickets = currentGame[7]
        dump.inning1Score = currentGame[8]
        dump.inning1Result = currentGame[9]
        dump.balls = currentGame[10]
        dump.innings = currentGame[11]
        dump.gameHappening = convertIntToBool(currentGame[12])
        
        dump.coinToss = convertIntToBool(currentGame[13])
        dump.tossDecision = convertIntToBool(currentGame[14])
        games.append(dump)
    conn.commit()
    conn.close()
    return games
def importGameValuesBackup():
    gameData = [] 
    with open('games.csv') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
  
      for row in csv_reader:
        gameData.append(row)
  
  
    print(gameData)
    games = []
    for n in range(len(gameData)):
        currentGame = gameData[n]
        dump = Game(int(currentGame[0]),currentGame[15],currentGame[16],int(currentGame[1]),int(currentGame[2]),int(currentGame[3]))
        dump.runs = int(currentGame[4])
        dump.bowlerNumber = int(currentGame[5])        
        dump.userTurn = int(currentGame[6])
        dump.currentInningWickets = int(currentGame[7])
        dump.inning1Score = int(currentGame[8])
        dump.inning1Result = currentGame[9]
        dump.balls = int(currentGame[10])
        dump.innings = int(currentGame[11])
        print("Game Happening")
        print(currentGame[12])
        dump.gameHappening = convertIntToBool(currentGame[12])
        
        dump.coinToss = convertIntToBool(currentGame[13])
        dump.tossDecision = convertIntToBool(currentGame[14])
        games.append(dump)

    return games
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Fake Cricket!'
    )

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # can be cached...
  

@client.event
async def on_message(message):
    global gameStarted
    global userTurn
    global bowlerNumber
    games = importGameValues()
    print(len(games))
    if(len(games)==0):
      games = importGameValuesBackup()
    isMod = False
    conn = sqlite3.connect('users.db', timeout=1)
    cursor = conn.cursor()
   
    Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
    conn.commit()

    for n in range(len(ModIds)):
        if message.author.id == ModIds[n]:
            isMod = True
    user = client.get_user(706698513710579762)
    channelId = 771559757592526891
    if "resume games" in message.content:
      print("WORKS")
      print(len(games))
      for n in range(len(games)):
        print(n)
        currentGame = games[n]
        print (currentGame.gameHappening)
        if(currentGame.gameHappening != True):
          return
        if(currentGame.coinToss == True):
          channel = client.get_channel(currentGame.channelId)
          output = "<@!"+ str(currentGame.player1) +">,please calls heads or tail"
          await channel.send(output)
          return
        if(currentGame.tossDecision == True):
          channel = client.get_channel
          (currentGame.channelId)
          output = "<@!"+ str(currentGame.player1) +">,please choose to bowl or bat"
          await channel.send(output)
          return
        else:
          if(currentGame.userTurn == 0):
            user = client.get_user(currentGame.player2)
            await user.send("Put in bowler number")
          else:
            channel = client.get_channel(currentGame.channelId)
            output = "<@!"+ str(currentGame.player1) +">, please input Swing Number"
            await channel.send(output)


    if message.author == client.user:
        return
    if "?add user" in message.content:
        if isMod == True:
               text = message.content.lower()
               text = text.replace("?add user","")
               playerInfo = text.split(',')
               playerInfo[0] = str(playerInfo[0])
               playerInfo[1] = int(playerInfo[1])
               await message.channel.send(playerInfo)
               Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
               print(len(Database))
               playerInDatabase = False
               for n in range(len(Database)):
                   if playerInfo[1] == Database[n][1]:
                       Database[n][0] == playerInfo
                       playerInDatabase = True
                       newTeamName = playerInfo[0]
                       playerId = playerInfo[1]
                       cursor.execute(
                           "UPDATE users SET teamName = ? WHERE userId = ?",
                           (newTeamName, playerId)
                           )
                       await message.channel.send("Player Team Changed")
               if playerInDatabase == False:
                       conn = sqlite3.connect('users.db', timeout=1)
                       cursor = conn.cursor()
                       input = "INSERT INTO users VALUES ('" + playerInfo[0]+"'," + str(playerInfo[1])+")"
                       await message.channel.send(input)
                       cursor.execute(input)
                       await message.channel.send("Player Added")
                       conn.commit()
                       
        return
            
    if "?start game," in message.content:
        for n in range(len(games)):
            if games[n].channelId == message.channel.id:
                if games[n].gameHappening == True:
                    return
        text = message.content.lower()
        text = text.replace("?start game","")
        players = text.split(',')
        team1 = ""
        team2 = ""
        
 
        for n in range(len(players)):
            for x in range(len(Database)):
                
                player = Database[x][0].lower()
                if player in players[n]:
                    if team1 == "" :
                        team1 = Database[x][1]
                        team1Name = Database[x][0]
                    else:
                        team2 = Database[x][1]
                        team2Name = Database[x][0]
        if team1 == "" or team2 == "":
            await message.channel.send("One of those teams doesn't exist")
            await message.channel.send(Database)
            return
        for n in range(len(games)):
            if(team1 == games[n].player1 or team1 == games[n].player2 or team2 == games[n].player1 or team2 == games[n].player2):
                await message.channel.send("One of the teams is already in a game")
                return
        newGame = Game(message.channel.id,team1Name,team2Name,team1,team2,len(games))
  
        await message.channel.send(len(games))
        await message.channel.send("gameStarted")
        await message.channel.edit(name = (team1Name + " vs. " + team2Name))
        output = "<@!"+ str(newGame.player1) +">,please calls heads or tail"
        await message.channel.send(output)
        games.append(newGame)
        await message.channel.send(newGame.player1)
        await message.channel.send(len(games))
        print(games)
        print(newGame.bowlerNumber)
        print(len(games))
        sendGameValues(games)
        return;

    isInGame = False
    currentGameId = -1
    for n in range(len(games)):
        if(message.author.id == games[n].player1 or message.author.id == games[n].player2):
            isInGame = True
            currentGameId = n
    if isInGame == False:
        return
    
    currentGame = games[currentGameId]
    if "end game" in message.content:
        if isMod == True:
            currentGame.gameHappening = False
            await message.channel.send("Game Ended")
            sendGameValues(games)
            return
    if currentGame.gameHappening == False:
        return

    if message.channel.id != currentGame.channelId and not isinstance(message.channel, discord.DMChannel):
       return 
    if currentGame.coinToss == True:
        
        if message.author.id != currentGame.player1:
            return
        if message.content.lower() == "heads" or message.content.lower() == "tails":
            coinToss = random.randint(0, 1)
            calledToss = 1
            currentGame.coinToss = False
            if(message.content.lower()=="heads"):
                calledToss = 0
            if(coinToss == calledToss):
                output = "<@!"+ str(currentGame.player1) +">,please choose to bowl or bat"
                
                await message.channel.send(output)
                sendGameValues(games)
                return
            else:
                 newPlayer2 = currentGame.player1
                 newPlayer1 = currentGame.player2
                 currentGame.player1 = newPlayer1
                 currentGame.player2 = newPlayer2
                 newTeam1 = currentGame.team2
                 newTeam2 = currentGame.team1
                 currentGame.team1 = newTeam1
                 currentGame.team2 = newTeam2
                 output = "<@!"+ str(currentGame.player1) +">,please choose to bowl or bat"
                
                 await message.channel.send(output)
                 sendGameValues(games)
                 return
            
        else:
            await message.channel.send("please calls heads or tails")
            return
         
        return
    if currentGame.tossDecision == True:
            if(message.author.id != currentGame.player1):
                return
            if message.content.lower() == "bowl" or message.content.lower() == "bat":
                currentGame.tossDecision = False
                if(message.content.lower() == "bowl"):
                    newPlayer2 = currentGame.player1
                    newPlayer1 = currentGame.player2
                    currentGame.player1 = newPlayer1
                    currentGame.player2 = newPlayer2
                    newTeam1 = currentGame.team2
                    newTeam2 = currentGame.team1
                    currentGame.team1 = newTeam1
                    currentGame.team2 = newTeam2
            
                    
                user = client.get_user(currentGame.player2)
                sendGameValues(games)
                await user.send("Please input bowler number")
            else:
                await message.channel.send("please choose to bowl or bat")
                return
            return
    if currentGame.userTurn == 0 and isinstance(message.channel, discord.DMChannel):
        if message.content.isnumeric():
            if int(message.content)>50 or int(message.content)<1:
                await message.channel.send("Put a number 1-50")
                return;
            currentGame.bowlerNumber = int(message.content)
        else:
            await message.channel.send("please input a number")
            return
        channel = client.get_channel(currentGame.channelId)
        output = "<@!"+ str(currentGame.player1) +">,please input Swing Number"
        await channel.send(output)
        currentGame.userTurn = 1
        sendGameValues(games)
        return
    if currentGame.userTurn == 1 and message.channel.id == currentGame.channelId and message.author.id == currentGame.player1:
        
        global wickets  
        if message.content.isnumeric():
            if int(message.content)>50 or int(message.content)<1:
                await message.channel.send("Put a number 1-50")
                return;
            writeup = ""
            output = ""
            response = abs(int(message.content)-currentGame.bowlerNumber)
            if response > 25 :
                response = 50-response
            if response < 2:
                writeup = sixWriteups[random.randint(0,len(sixWriteups)-1)]
                output = "Six!"
                currentGame.runs += 6
            elif response < 5:
                output = "Four"
                writeup = fourWriteups[random.randint(0,len(fourWriteups)-1)]
                currentGame.runs += 4
                
            elif response < 6:
                output = "Three"
                currentGame.runs += 3
                writeup = threeWriteups[random.randint(0,len(threeWriteups)-1)]
            elif response < 9:
                output ="Two"
                currentGame.runs += 2
                writeup = twoWriteups[random.randint(0,len(twoWriteups)-1)]
            elif response <15:
                output = "One"
                currentGame.runs += 1
                writeup = oneWriteups[random.randint(0,len(oneWriteups)-1)]
            elif response <24:
                output = "Dot"
                currentGame.runs += 0
                writeup = dotBallWriteups[random.randint(0,len(dotBallWriteups)-1)]
            else:
                output = "Wicket"
                currentGame.runs += 0
                currentGame.currentInningWickets += 1
                writeup = wicketWriteups[random.randint(0,len(wicketWriteups)-1)]
                                            # can be cached..
            currentGame.balls += 1
            overs = int((currentGame.balls-1)/6)
            balls = currentGame.balls%6
            if balls == 0:
                balls =6
            
            runs = currentGame.runs
            currentGame.userTurn = 0
            currentScore =writeup+"\n"+ output+"\n"+"Bowler number: "+str(currentGame.bowlerNumber)+"\n"+"Batter number: "+str(int(message.content))+"\n"+"Difference: "+str(response)+"\n"+str(overs)+"."+str(balls)+"  "+str(runs)+"/"+str(currentGame.currentInningWickets)
            currentScore += "\n" + "Run Rate:" + str(round(6*runs/currentGame.balls,2))
            if(currentGame.innings==2 and 60>balls):
               currentScore += "\n" + "Runs Needed:" + str(1+currentGame.inning1Score-runs) 
               currentScore += "\n" + "Required Run Rate:" + str(round(6*(currentGame.inning1Score-runs)/(60-currentGame.balls),2))
            await message.channel.send(currentScore)
   
            if(currentGame.innings == 1):
                if(currentGame.balls >=60 or currentGame.currentInningWickets >= 5):
                    await message.channel.send("Innings is over, "+str(runs) +" runs scored")
                    currentGame.inning1Result = str(runs)+"/"+str(currentGame.currentInningWickets) + " (" + str(overs)+"."+ str(balls) + ")"
                    currentGame.innings = 2
                    currentGame.inning1Score = runs
                    currentGame.balls = 0
                    currentGame.currentInningWickets = 0
                    newPlayer2 = currentGame.player1
                    newPlayer1 = currentGame.player2
                    currentGame.player1 = newPlayer1
                    currentGame.player2 = newPlayer2
                    currentGame.runs=0
            else:
                if(currentGame.balls >=60 or currentGame.currentInningWickets >= 5 or runs>currentGame.inning1Score):
                    innings2Result = str(runs)+"/"+str(currentGame.currentInningWickets) + " (" + str(overs)+"."+ str(balls) + ")"
                    if(runs>currentGame.inning1Score):
                        await message.channel.send(currentGame.team2+" wins by" + str(5-currentGame.currentInningWickets)+" wickets")
                        await message.channel.send(currentGame.team1 + ": " + currentGame.inning1Result)
                        await message.channel.send(currentGame.team2 + ": " + innings2Result)
                
                    else:
                        await message.channel.send(currentGame.team1+" wins by"+ str(currentGame.inning1Score-runs)+" runs")
                        await message.channel.send(currentGame.team1 + ": " + currentGame.inning1Result)
                        await message.channel.send(currentGame.team2 + ": " + innings2Result)
                    currentGame.gameHappening = False
                    sendGameValues(games)
                    return
        
            user = client.get_user(currentGame.player2)
            await user.send(currentScore)
            await user.send("Put in bowler number")
            sendGameValues(games)

keep_alive()
client.run(TOKEN)