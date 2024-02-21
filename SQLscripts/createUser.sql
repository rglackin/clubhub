CREATE TABLE user (
	ID INTEGER PRIMARY KEY,
	username TEXT not null,
	password TEXT not null,
	phone_no TEXT not null,
	email TEXT not null,
	is_admin BOOLEAN DEFAULT 0,
	user_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)
