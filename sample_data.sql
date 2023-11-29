INSERT INTO app_user (user_id, username, password, profile_img, bio)
VALUES
    (1, 'Aaron', 'Rodgers', 'img1', 'My bio 1'),
    (2, 'Jordan', 'Love', 'img2', 'My bio 2')
;

SELECT * FROM app_user;


INSERT INTO event (event_id, title, date, time, image_link, author_id, public)
VALUES
    (1, 'Football', '11/28/2023', '10:00pm', 'image link', 1, true)
;

SELECT * FROM event;


INSERT INTO participating_in (participating_id, user_id, event_id)
VALUES
    (1, 1, 1),
    (2, 2, 1)
;

SELECT * FROM participating_in;


INSERT INTO friends (friend_id, user1_id, user2_id)
VALUES
    (1, 1, 2)
;

SELECT * FROM friends;