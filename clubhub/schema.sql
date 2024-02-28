CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
CREATE TABLE IF NOT EXISTS "events" ("event_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "event_name" varchar(20) NOT NULL, "description" varchar(400) NOT NULL, "date" date NULL, "time" time NULL, "venue" varchar(30) NOT NULL, "event_created" datetime NOT NULL, "event_updated" datetime NOT NULL, "club_id" integer NOT NULL REFERENCES "club" ("club_id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "events_club_id_95a77c27" ON "events" ("club_id");
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE TABLE user (

	ID INTEGER PRIMARY KEY,

	username TEXT UNIQUE not null,

	password TEXT not null,

	phone_no TEXT UNIQUE not null,

	email TEXT UNIQUE not null,

	is_admin BOOLEAN DEFAULT 0,

	approved BOOLEAN DEFAULT FALSE,

	user_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	user_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

	);
CREATE TRIGGER set_as_admin

AFTER INSERT ON USER 

BEGIN

	UPDATE user

    SET is_admin = TRUE, approved = TRUE

    WHERE ID = NEW.ID AND (SELECT COUNT(*) FROM user) = 1;

END;
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
CREATE TABLE club(

club_id INTEGER PRIMARY KEY,

name VARCHAR(20) UNIQUE,

description VARChaR(100),



created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

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

JOIN user u ON cu.user_ID = u.ID
/* club_membership_info(membership_id,club_id,club_name,club_description,user_id,username,phone_no,email,is_coord,membership_approved) */;
