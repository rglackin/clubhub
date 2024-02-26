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
