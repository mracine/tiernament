DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS round;
DROP TABLE IF EXISTS player;

CREATE TABLE game (
  uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
  name TEXT,
  time INTEGER,
  game TEXT,
  tier BLOB,
  players BLOB,
  rounds BLOB,
  params BLOB
);

CREATE TABLE round (
  uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
  gameid TEXT NOT NULL,
  number INTEGER,
  placements BLOB
);

CREATE TABLE player (
  uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
  name TEXT,
  icon BLOB,
  color TEXT
);

