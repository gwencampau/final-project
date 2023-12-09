from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class app_user(db.Model):
    # user_id SERIAL,
    user_id = db.Column(db.Integer, primary_key=True)
    # email VARCHAR(50) NOT NULL,
    email = db.Column(db.String(255), nullable=False)
    # username VARCHAR(20) NOT NULL,
    username = db.Column(db.String(20), nullable=False, unique=True)
    # password VARCHAR(255) NOT NULL,
    password = db.Column(db.String(255), nullable=False)
    # profile_img VARCHAR(10) NULL, --Postgres does not support BLOB so I had to find an alternative
    profile_img = db.Column(db.LargeBinary, nullable=True)
    # bio VARCHAR(150) NULL,
    bio = db.Column(db.String(150), nullable=True)

    def __init__(self, email: str, username: str, password: str, profile_img: str, bio: str):
        self.email = email
        self.username = username
        self.password = password
        self.profile_img = profile_img
        self.bio = bio

    def __repr__(self) -> str:
        return f'User({self.user_id}, {self.email}, {self.username}, {self.password}, {self.profile_img}, {self.bio})'




class event(db.Model):
    # event_id SERIAL,
    event_id = db.Column(db.Integer, primary_key=True)
    # title VARCHAR(50) NOT NULL,
    title = db.Column(db.String(50), nullable=False)
    # date DATE NOT NULL,
    date = db.Column(db.Date, nullable=False)
    # time TIME NOT NULL,
    time = db.Column(db.Time, nullable=False)
    # image_link VARCHAR(500) NULL, --I made this varchar instead of bytea since currently our images work by submitting a link
    image_link = db.Column(db.String(500), nullable=True)
    # description VARCHAR(255) NULL,
    description = db.Column(db.String(150), nullable=True)
    # tags TEXT[] NULL
    tags = db.Column(db.ARRAY(db.String))
    # author_id INT NOT NULL,
    # FOREIGN KEY (author_id) REFERENCES app_user(user_id) ON UPDATE CASCADE ON DELETE SET NULL
    author_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    user = db.relationship('app_user', backref='author')
    # public BOOLEAN NOT NULL,
    public = db.Column(db.Boolean, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    def __init__(self, title: str, date: str, time: str, image_link: str, description: str, tags: list, author_id: int, public: bool, location: str):
        self.title = title
        self.date = date
        self.time = time
        self.image_link = image_link
        self.description = description
        self.tags = tags
        self.author_id = author_id
        self.public = public
        self.location = location
    
    def __repr__(self) -> str:
        return f'Event({self.event_id}, {self.title}, {self.date}, {self.time}, {self.image_link}, {self.description}, {self.author_id}, {self.public}, {self.location})'
    


class participatingIn(db.Model):
    # participating_id SERIAL,
    participating_id = db.Column(db.Integer, primary_key=True)
    # user_id INT NOT NULL,
    # FOREIGN KEY (user_id) REFERENCES app_user(user_id),
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    user = db.relationship('app_user', backref='participant')
    # event_id INT NOT NULL,
    # FOREIGN KEY (event_id) REFERENCES event(event_id)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    event = db.relationship('app_user', backref='event')
    # PRIMARY KEY (user_id, event_id),

    def __init__(self, user_id: int, event_id: int):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self) -> str:
        return f'Participating In({self.participating_id}, {self.user_id}, {self.event_id})'


# Multiple Foreign Keys: https://stackoverflow.com/questions/22355890/sqlalchemy-multiple-foreign-keys-in-one-mapped-class-to-the-same-primary-key
class friends(db.Model):
    # friend_id SERIAL,
    # PRIMARY KEY (friend_id),
    friend_id = db.Column(db.Integer, primary_key=True)
    # user1_id INT NOT NULL,
    # FOREIGN KEY (user1_id) REFERENCES app_user(user_id),
    user1_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    user1 = db.relationship('app_user', foreign_keys=[user1_id],backref='user1')
    # user2_id INT NOT NULL,
    # FOREIGN KEY (user2_id) REFERENCES app_user(user_id)
    user2_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    user2 = db.relationship('app_user', foreign_keys=[user2_id], backref='user2')

    def __init__(self, user1_id: int, user2_id: int):
        self.user1_id = user1_id
        self.user2_id = user2_id

    def __repr__(self) -> str:
        return f'Friends({self.friend_id}, {self.user1_id}, {self.user2_id})'