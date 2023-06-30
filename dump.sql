CREATE TABLE users(
	id serial PRIMARY KEY,
	username VARCHAR ( 64 ) UNIQUE NOT NULL,
	email VARCHAR ( 64 ) UNIQUE NOT NULL,
	password_hash VARCHAR ( 128 ) NOT NULL
);

CREATE TABLE player(
	id serial PRIMARY KEY, 
	player_name VARCHAR(32),
	pos VARCHAR(32),
	team VARCHAR(32), 
	opponent VARCHAR(32), 
	home BOOLEAN, 
	proj_std REAL,
	avg_rank_std REAL,
	sdev_rank_std REAL,
  	proj_half REAL,
	avg_rank_half REAL,
	sdev_rank_half REAL,
	proj_ppr REAL,
	avg_rank_ppr REAL,
	sdev_rank_ppr REAL	 
);

CREATE TABLE roster (
	id serial PRIMARY KEY, 
	user_id INTEGER, 
	player_id INTEGER, 
	FOREIGN KEY(player_id) REFERENCES player (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE opponent_roster (
	id serial PRIMARY KEY, 
	user_id INTEGER, 
	player_id INTEGER, 
	FOREIGN KEY(player_id) REFERENCES player (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE league (
	id serial PRIMARY KEY, 
	user_id INTEGER UNIQUE NOT NULL, 
	qb INTEGER, 
	rb INTEGER, 
	wr INTEGER, 
	te INTEGER, 
	rb_wr INTEGER, 
	wr_te INTEGER, 
	rb_te INTEGER, 
	dst INTEGER, 
	kicker INTEGER, 
	scoring VARCHAR(32), 
	rb_wr_te INTEGER, 
	qb_rb_wr_te INTEGER, 
	FOREIGN KEY(user_id) REFERENCES users (id)
);