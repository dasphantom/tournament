-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--create database
DROP DATABASE IF EXISTS tournament;


CREATE DATABASE tournament;
\c tournament;

--create players table
CREATE TABLE players (
playerID SERIAL PRIMARY KEY,
name text,
wins smallint default 0,
matches smallint default 0
);

--create matches table
CREATE TABLE matches (
matchID SERIAL PRIMARY KEY,
winner integer REFERENCES players (playerID),
loser integer REFERENCES players (playerID)
);
