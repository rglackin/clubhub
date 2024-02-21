CREATE TABLE club_user (
club_id INTEGER,
ID INTEGER,
created TIME,
updated TIME,
FOREIGN KEY (club_id) REFERENCES club(club_id),
FOREIGN KEY (ID) REFERENCES user(ID))