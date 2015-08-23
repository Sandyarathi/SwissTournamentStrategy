#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute_query(query,variables=(), fetch=False, commit=False):
    """Helper function to execute a required query by establishing the database connection"""
    dbConnection=connect()
    cursor=dbConnection.cursor()
    if len(variables)==0:
        cursor.execute(query)
    else:
        cursor.execute(query,variables)
    if(fetch):
        fetched=cursor.fetchall()
    else:
        fetched=None
    if(commit):
        dbConnection.commit()
    dbConnection.close()
    return fetched


def deleteMatches():
    """Remove all the match records from the database."""
    query="DELETE from matches_info;"
    execute_query(query,commit=True)


def deletePlayers():
    """Remove all the player records from the database."""
    query="DELETE from registered_players;"
    execute_query(query,commit=True)



def countPlayers():
    """Returns the number of players currently registered."""
    query="SELECT count(*) as numOfPlayers FROM registered_players;"
    result=execute_query(query,fetch=True)
    count= result[0][0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO registered_players (player_name) VALUES (%s)"
    execute_query(query,variables=(name,),commit=True)



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

    """Code Logic: 
        The rows fetched from the player_match_record view is populated into 
        a list. 
    """
    query="SELECT * FROM player_match_record ORDER BY wins DESC;"
    queryResult=execute_query(query,fetch=True)
    list_of_playerRecords=[]
    for row in queryResult:
        listTuple=(row[0],row[1],row[3],row[2])
        list_of_playerRecords.append(listTuple)
    return list_of_playerRecords


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    """Code Logic:
            The queries insert records of each match played along with the winner and loser
            and also updates the registered players table wins column of winner of the match.
    """
    query1="INSERT INTO matches_info(player_id,match_result) VALUES (%s,%s)"
    query2="INSERT INTO matches_info(player_id,match_result) VALUES (%s,%s)"
    query3="UPDATE registered_players SET wins=wins+1 where player_id=(%s)"
    execute_query(query1,variables=(winner,1),commit=True)
    execute_query(query2,variables=(loser,0),commit=True)
    execute_query(query3,variables=(winner,),commit=True)
 
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

    """
    Code Logic:
        The records from the player_match_record is fetched in the decending order of wins and for each adjacent rows
        the pairing list is appended with a new pair.
    """
    query="SELECT * FROM player_match_record ORDER BY wins DESC;"
    queryResult=execute_query(query,fetch=True)
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
    return pairs


