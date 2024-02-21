CREATE TRIGGER set_first_user_as_admin
AFTER INSERT ON user
BEGIN
    UPDATE user
    SET admin = TRUE
    WHERE ID = NEW.ID AND (SELECT COUNT(*) FROM user) = 1;
END;
