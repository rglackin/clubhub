CREATE TABLE club(
club_id INTEGER PRIMARY KEY,
name VARCHAR(20) UNIQUE,
description VARChaR(100),

created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE user (
	ID INTEGER PRIMARY KEY,
	username TEXT UNIQUE not null,
	password TEXT not null,
	phone_no TEXT UNIQUE not null,
	email TEXT UNIQUE not null,
	is_admin BOOLEAN DEFAULT 0,
	is_approved BOOLEAN DEFAULT FALSE,
	user_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
CREATE TABLE events(
event_id INTEGER PRIMARY KEY,

event_name VARCHAR(20),
description VARCHAR(100),
date DATE,
time TIME,
venue VARCHAR(30),
event_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
event_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
CREATE TABLE club_user (
id INTEGER PRIMARY KEY,
club_id INTEGER,
user_ID INTEGER,
is_coord BOOLEAN,
is_approved BOOLEAN,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (club_id) REFERENCES club(club_id),
FOREIGN KEY (user_ID) REFERENCES user(ID)
);
CREATE TABLE event_user(
id INTEGER PRIMARY KEY,
user_id INTEGER,
event_id INTEGER,
is_approved BOOLEAN DEFAULT False,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (event_id) REFERENCES events(event_id),
FOREIGN KEY (user_id) REFERENCES user(ID)
);
CREATE TRIGGER set_as_admin
AFTER INSERT ON USER 
BEGIN
	UPDATE user
    SET is_admin = TRUE, approved = TRUE
    WHERE ID = NEW.ID AND (SELECT COUNT(*) FROM user) = 1;
END;
CREATE TRIGGER event_approval
AFTER INSERT ON event_user
FOR EACH ROW
BEGIN
	UPDATE event_user
    SET is_approved = 1
    WHERE event_id = NEW.event_id
    AND user_id IN (
        SELECT user_ID
        FROM club_user
        WHERE club_id = (
            SELECT club_id
            FROM events
            WHERE event_id = NEW.event_id 
        ) AND is_approved = TRUE
    );
END;
CREATE VIEW club_membership_info AS
SELECT cu.id AS membership_id,
       c.club_id,
       c.name AS club_name,
       c.description AS club_description,
       u.ID AS user_id,
       u.username,
       u.phone_no,
       u.email,
       cu.is_coord,
       cu.is_approved AS membership_approved
FROM club_user cu
JOIN club c ON cu.club_id = c.club_id
JOIN user u ON cu.user_ID = u.ID;