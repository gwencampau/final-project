CREATE DATABASE communifree;

CREATE TABLE app_user (
    user_id SERIAL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_img bytea NULL, --Postgres does not support BLOB so I had to find an alternative
    bio VARCHAR(150) NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE event (
    event_id SERIAL,
    title VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    image_link VARCHAR(500) NULL, --I made this varchar instead of bytea since currently our images work by submitting a link
    description VARCHAR(255) NULL,
    author_id INT NOT NULL,
    tags TEXT[] NULL,
    public BOOLEAN NOT NULL,
    location VARCHAR(255) NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY (author_id) REFERENCES app_user(user_id)
);

CREATE TABLE participating_in(
    participating_id SERIAL,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    PRIMARY KEY (participating_id),
    FOREIGN KEY (user_id) REFERENCES app_user(user_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

CREATE TABLE friends(
    friend_id SERIAL,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    PRIMARY KEY (friend_id),
    FOREIGN KEY (user1_id) REFERENCES app_user(user_id),
    FOREIGN KEY (user2_id) REFERENCES app_user(user_id)
);