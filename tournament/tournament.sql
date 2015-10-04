-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players(
	id serial primary key,
	name text,
	win integer,
	lose integer,
	matches integer);

create table matches(
	p1_id integer references players(id),
	p2_id integer references players(id),
	winner_id integer,
	loser_id integer);