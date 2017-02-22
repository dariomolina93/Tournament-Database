-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--If the database exists delete it
DROP DATABASE IF EXISTS tournament;

--create the database
CREATE DATABASE tournament;

--connect to the database
\c tournament;


--create players table with the appropiate attributes
CREATE TABLE players (
id serial not null primary key,
name text
);

--create players table with appropiate attributes
CREATE TABLE matches(
match_id serial not null primary key,
winner_id serial not null references players,
loser_id serial not null references players
);

CREATE TABLE statistics(
	id serial not null references players,
	wins integer not null,
	loses integer not null
);