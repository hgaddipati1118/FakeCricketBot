"""
Created on Sat Oct 31 15:59:56 2020

@author: Harsha Gaddipati
"""
import sqlite3

def makeTables():
  
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()
  cursor.execute('DELETE FROM games;',);
  conn.commit()
  conn.close()
  return
  cursor.execute('DELETE FROM users;',);
  #cursor.execute("CREATE TABLE users (teamName TEXT, userId INTEGER)")
 # cursor.execute("CREATE TABLE games (channelId INTEGER, player1 INTEGER, player2 INTEGER, gameId INTEGER, runs INTEGER, bowlerNumber INTEGER, userTurn INTEGER, currentInningsWickets INTEGER, inning1Score INTEGER, inning1Result TEXT, balls INTEGER, innings INTEGER, gameHappening INTEGER, coinToss INTEGER, tossDecision INTEGER, team1 TEXT, team2 TEXT )")
  cursor.execute("INSERT INTO users VALUES ('Sunrisers Hyderbad',706698513710579762)")
  cursor.execute("INSERT INTO users VALUES ('Omaha Union',340541260672532482)")
  cursor.execute("INSERT INTO users VALUES ('Carolina Cricketeers',701221250776825856)")
  cursor.execute("INSERT INTO users VALUES ('Lake Frozen',612494299120140295)")
  cursor.execute("INSERT INTO users VALUES ('Chesire',202273074261917697)")
  cursor.execute("INSERT INTO users VALUES ('Arizona Scorpions',477216596667006996)")
  cursor.execute("INSERT INTO users VALUES ('Army Black Knights',534010044182822914)")

  cursor.execute("INSERT INTO users VALUES ('Super 11',715243714003337296)")
  cursor.execute("INSERT INTO users VALUES ('Chincinnati Nega Chins',652016781690404884)")
  cursor.execute("INSERT INTO users VALUES ('Columbus Cricket Club',404782639824764951)")
  cursor.execute("INSERT INTO users VALUES ('Superzakers',740781497048629270)")
  cursor.execute("INSERT INTO users VALUES ('DELHI DAREDEVILS',756157157501567118)")
  cursor.execute("INSERT INTO users VALUES ('Canadian Cricket Cowboys',636749752683200523)")
  cursor.execute("INSERT INTO users VALUES ('Pakistani Falcons',293778672807182336)")
  cursor.execute("INSERT INTO users VALUES ('Souf CC',237234603981537280)")
  cursor.execute("INSERT INTO users VALUES ('C0ldspark',195544830481268736)")
  cursor.execute("INSERT INTO users VALUES ('Calypso Kings',716465822020665405)")
  cursor.execute("INSERT INTO users VALUES ('New Delhi Superstars',306609698340339714)")
  cursor.execute("INSERT INTO users VALUES ('KBK Stallions',715094998617686036)")
  cursor.execute("INSERT INTO users VALUES ('schizo d dharms',532472438718464001)")
  cursor.execute("INSERT INTO users VALUES ('Sydney Sixers',105545186028822528)")
  cursor.execute("INSERT INTO users VALUES ('Tajikistan Royals',352849361920851968)")
  cursor.execute("INSERT INTO users VALUES ('Red Star Laos',144969605977341953)")
  cursor.execute("INSERT INTO users VALUES ('Connacht Cricket ',409350943788892160)")
  Database = cursor.execute("SELECT teamName, userId FROM users").fetchall()
  print(len(Database))
  conn.commit()
  conn.close()
 

ModIds = [340541260672532482,706698513710579762,701221250776825856,202273074261917697,477216596667006996,534010044182822914,636749752683200523]
