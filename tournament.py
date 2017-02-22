#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    #establish a connection with the database
    connection = connect();

    #get cursor to execute queries
    cursor = connection.cursor()

    #delete all the information from matches table
    cursor.execute("DELETE FROM matches;")

    #commit to prevent any rollbacks
    connection.commit()

    #update players table 
    cursor.execute("update statistics set wins = 0, loses = 0;")

    #commit to prevent any rollbacks
    connection.commit()

    connection.close()



def deletePlayers():
    """Remove all the player records from the database."""

    #establish the connection
    connection = connect()

    #obtain the cursor to perform the queries
    cursor = connection.cursor()

    #first need to delete statistics to prevent any key dependant error since id is reference to players.
    cursor.execute("DELETE FROM statistics;")

    #commit to prevent any rollbacks
    connection.commit()

    #delete all data from players table
    cursor.execute("DELETE FROM players;")
    connection.commit()


    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""

    #establish a connection
    connection = connect()

    #obtain the cursor to perform queries in database
    cursor = connection.cursor()

    #count the players registered
    cursor.execute("select count(id) as num from players;")

    #get the resulting table and storing it
    value = cursor.fetchone()[0]
    connection.close()

    #return the first value of querie since its the amount of players in table
    return value 
    
countPlayers()

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    #bleached the name to prevent any malicious user input
    name = bleach.clean(name, strip = True)

    #established a connection
    connection = connect()

    #obtain cursor to perform queries in database
    cursor = connection.cursor()

    #insert data into table, "register player"
    cursor.execute("insert into players(name) values(%s);", (name,))
    connection.commit()

    #insert into statistics table initial values since they haven't played yet.
    cursor.execute("insert into statistics(wins, loses) values(0,0);")

    #commit to prevent any rollbacks
    connection.commit()

    connection.close()

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

    #establish a connection
    connection = connect()

    #obtain the cursor to perform the queries
    cursor = connection.cursor()

    #querie that returns players and their win records sorted by wins
    cursor.execute("select players.id, players.name, statistics.wins, (statistics.wins + statistics.loses) as totalGames from players join statistics on players.id = statistics.id order by wins;")

    #store the results of the query 
    standings = cursor.fetchall()

    connection.close()

    return standings 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    #establish a connection
    connection = connect()

    #obtain the cursor to perform queries
    cursor = connection.cursor()

    #insert into table matches the match between winner and loser
    cursor.execute("insert into matches(winner_id, loser_id) values (%s,%s);", (winner,loser,))
   
    #commit to prevent any rollbacks
    connection.commit()

    #update the information in the players table based on the winner and loser
    cursor.execute("update statistics set wins = wins + 1 where id = %s;", (winner,))
    connection.commit()

    #update information in players table for loser
    cursor.execute("update statistics set loses = loses + 1 where id = %s;", (loser,))
    connection.commit()


    connection.close()


 
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

    #obtain the standing of each player
    standings = playerStandings()

    #create a list the will store the tuples of the players for the next round
    pairings = []

    #iterate through the standing and pair up the players
    for i in range(0, len(standings) - 1, 2):

        #create a tuple object and obtain the information from first player and second player
        l = (standings[i][0],standings[i][1], standings[i + 1][0], standings[i + 1][1]);

        #store that tuple in list
        pairings.append(l)

    return pairings