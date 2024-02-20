CREATE TABLE club_events (
club_id INTEGER,
event_name INTEGER,
created TIME,
updated TIME,
FOREIGN KEY (club_id) REFERENCES club(club_id),
FOREIGN KEY (event_name) REFERENCES events(event_name))
