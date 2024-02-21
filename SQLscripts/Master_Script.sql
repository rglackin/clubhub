CREATE TABLE club(
club_id INT Primary key,
name VARCHAR(20),
description VARChaR(100),
validity_status BOOLEAN,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE user (
	ID INTEGER PRIMARY KEY,
	username TEXT not null,
	password TEXT not null,
	phone_no TEXT not null,
	email TEXT not null,
	is_admin BOOLEAN DEFAULT 0,
	user_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
CREATE TABLE events(
event_id INTEGER PRIMARY KEY,
fk_club INTEGER,
event_name VARCHAR(20),
description VARCHAR(100),
date DATE,
time TIME,
venue VARCHAR(30),
event_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
event_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (fk_club) REFERENCES club(club_id)
);
CREATE TABLE club_user (
club_id INTEGER,
user_ID INTEGER,
is_coord BOOLEAN,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (club_id) REFERENCES club(club_id),
FOREIGN KEY (user_ID) REFERENCES user(ID)
);

CREATE TRIGGER set_first_user_as_admin
AFTER INSERT ON user
BEGIN
    UPDATE user
    SET is_admin = TRUE
    WHERE ID = NEW.ID AND (SELECT COUNT(*) FROM user) = 1;
END;