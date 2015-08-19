#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("DELETE from matches_info;")
    dbConnection.commit()
    cursor.close()
    dbConnection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("DELETE from registered_players;")
    dbConnection.commit()
    cursor.close()
    dbConnection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("SELECT count(*) as numOfPlayers FROM registered_players")
    count=cursor.fetchall()[0][0]
    cursor.close()
    dbConnection.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("INSERT INTO registered_players (player_name) VALUES (%s)", (name,))
    dbConnection.commit()
    cursor.close()
    dbConnection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("SELECT registered_players.player_id,registered_players.player_name,COUNT(matches_info.player_id) as matches_played, SUM(matches_info.match_result) as winCount "
                    "FROM registered_players LEFT OUTER JOIN matches_info ON (matches_info.player_id=registered_players.player_id) GROUP BY registered_players.player_id ORDER BY winCount DESC;")
    queryResult=cursor.fetchall()
    list_of_playerRecords=[]
    for row in queryResult:
        if row[3]==None:
            wins=0
        else:
            wins=row[3]
        listTuple=(row[0],row[1],wins,row[2])
        list_of_playerRecords.append(listTuple)
    cursor.close()
    dbConnection.close()
    return list_of_playerRecords


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("INSERT INTO matches_info(player_id,match_result) VALUES (%s,%s)", (winner,1,))
    cursor.execute("INSERT INTO matches_info(player_id,match_result) VALUES (%s,%s)", (loser,0,))
    dbConnection.commit()
    cursor.close()
    dbConnection.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    dbConnection=connect()
    cursor=dbConnection.cursor()
    cursor.execute("SELECT registered_players.player_id, registered_players.player_name, COUNT(matches_info.player_id) as total_matches, SUM(matches_info.match_result) as wins FROM registered_players LEFT OUTER JOIN matches_info ON "
                   "(matches_info.player_id = registered_players.player_id) GROUP BY registered_players.player_id ORDER BY wins DESC;")
    queryResult=cursor.fetchall()
    pairs=[]
    count=0
    for row in queryResult:
        if(count==0):
            id=row[0]
            name=row[1]
        else:
            tuple=(id,name,row[0],row[1])
            pairs.append(tuple)
        if(count==1):
            count=0
        else:
            count=count+1
    cursor.close()
    dbConnection.close()
    return pairs


