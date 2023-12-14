INSERT INTO app_user (user_id, email, username, password, profile_img, bio)
VALUES
    (1, 'arod@example.com', 'Aaron', 'Rodgers', 'img1', 'My bio 1'),
    (2, 'jlove@example.com', 'Jordan', 'Love', 'img2', 'My bio 2')
;

SELECT * FROM app_user;


INSERT INTO event (event_id, title, date, time, image_link, description, author_id, tags, public, location, latitude, longitude)
VALUES
    (1, 'Football', '11/28/2023', '10:00pm', 'https://www.fisu.net/app/uploads/2023/08/american_football.jpg', 'Let us play football outside in my backyard!', 1, ARRAY['cool', 'fun'], true, '8700 Phillips Rd, Charlotte, NC', null, null),
    (2, 'Superbowl Watch Party', '02/11/2024', '08:00pm', 'https://e1.365dm.com/17/01/2048x1152/skysports-super-bowl_3879214.jpg', 'Superbowl night! Who is going to win! Watch with us!',2, ARRAY['cool', 'sports'], true, '9029 Craver Rd, Charlotte, NC', null, null),
    (3, 'Football 2', '12/28/2023', '10:00pm', 'https://www.fisu.net/app/uploads/2023/08/american_football.jpg', 'Let us play football outside in my backyard!', 1, ARRAY['cool', 'fun'], true, '8917 Johnson Alumni Way', null, null),
    (4, 'Superbowl', '02/13/2024', '08:00pm', 'https://e1.365dm.com/17/01/2048x1152/skysports-super-bowl_3879214.jpg', 'Superbowl night! Who is going to win! Watch with us!',2, ARRAY['cool', 'sports'], true, '9137 Mary Alexander Rd, Charlotte, NC', null, null)
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