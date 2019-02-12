DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS round;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS tier;

CREATE TABLE game (
  id TEXT PRIMARY KEY UNIQUE NOT NULL,
  name TEXT,
  time INTEGER,
  game TEXT,
  tier BLOB,
  players BLOB,
  rounds INTEGER,
  params BLOB
);

CREATE TABLE round (
  id TEXT PRIMARY KEY UNIQUE NOT NULL,
  game_id TEXT NOT NULL,
  round_num INTEGER,
  placements BLOB
);

CREATE TABLE player (
  name TEXT PRIMARY KEY UNIQUE NOT NULL,
  icon BLOB,
  color TEXT
);

CREATE TABLE tier (
  id TEXT PRIMARY KEY UNIQUE NOT NULL,
  game TEXT,
  fighter TEXT,
  rank INTEGER,
  tier_group TEXT,
  img_url TEXT
);
