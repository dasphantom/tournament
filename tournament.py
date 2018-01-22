#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    list = [1,2,3]
    print list

    tup = (4,5,6)
    print tup

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from matches table and players table."""
    conn = connect();
    c = conn.cursor();

    c.execute("delete from matches;");
    conn.commit()

    c.execute("""
    update players
    set wins = 0, matches = 0
    ;""")
    conn.commit()

    conn.close();


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect();
    c = conn.cursor();
    c.execute("delete from players;");
    conn.commit()
    conn.close();


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect();
    c = conn.cursor();
    c.execute("select count(name) from players;");
    temp = c.fetchone();
    conn.close
    return temp[0];



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect();
    c = conn.cursor();
    c.execute("""
        insert into players(name)
        values (%s);
        """,
        (name,))
    conn.commit()
    conn.close();


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
    conn = connect();
    c = conn.cursor();
    c.execute("""
        select * from players
        order by wins desc
        ;""")
    temp = c.fetchall();
    conn.close();
    return temp

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    "//update matches table"
    conn = connect();
    c = conn.cursor();


    c.execute("""
        insert into matches(winner,loser)
        values (%s,%s);
        """,
        (winner,loser))
    conn.commit()

    "//update players table for winner"

    c.execute("""
        update players
        set wins = wins + 1, matches = matches + 1
        where playerID=%s
        ;""",
        (winner,))
    conn.commit()

    "//update players table for loser"

    c.execute("""
        update players
        set matches = matches + 1
        where playerID=%s
        ;""",
        (loser,))
    conn.commit()

    conn.close()

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

    step 1: setup an empty list
    """
    list= []

    "step 2: in this list we need to add tuples, contains id1, name1, id2, name2"
    "retrieve player id, name for all players"

    conn = connect()
    c = conn.cursor()

    "first count how many players we have"
    numberPlayers = countPlayers() / 2

    c.execute("""select playerID, name from players
    order by wins desc
    ;""")

    "now fetch the first two result and add this as a tuple together to list"
    "we need to create a loop for numberplayer / 2 "
    "fetchone creates a tuple already = double tuple"
    "we need to pass the tuple directly into the list "

    for x in range (0,numberPlayers):
        #tup = (c.fetchone(), c.fetchone())
        list.append(c.fetchone() + c.fetchone())


    conn.close()

    return list
