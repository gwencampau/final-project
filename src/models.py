from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#the flask-sqlalchemy documentation recommended creating an association table for a many-to-many relationship
#but I do not know how to link it to our database table called partcipatingIn or if I even need to since we have this
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
metadata_obj = db.MetaData()
participating_in = db.Table(
    "participatingIn",
    metadata_obj,
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), primary_key=True),
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id"), primary_key=True)
)

class AppUser(db.Model):
    __tablename__ = 'app_user'
    # user_id SERIAL,
    user_id = db.Column(db.Integer, primary_key=True) # Not sure how to do serial stuff
    # username VARCHAR(20) NOT NULL,
    username = db.Column(db.String(20), nullable=False)
    # password VARCHAR(255) NOT NULL,
    password = db.Column(db.String(255), nullable=False)
    # profile_img bytea NULL,
    profile_img = db.Column(db.LargeBinary, nullable=True) # Having issues with the BYTEA thing here
    # bio VARCHAR(150) NULL,
    bio = db.Column(db.String(150), nullable=True)
    # PRIMARY KEY (user_id)
    #relationships
    created_events=db.relationship("Event", backref='app_user', lazy=True)
    attending_events = db.relationship('Event', secondary=participating_in, lazy='subquery',
        backref=db.backref('event', lazy=True))
    

class Event(db.Model):
    __tablename__='event'
    # event_id SERIAL,
    event_id = db.Column(db.Integer, primary_key=True)
    # title VARCHAR(50) NOT NULL,
    title = db.Column(db.String(50), nullable=False)
    # date DATE NOT NULL,
    date = db.Column(db.Date, nullable=False)
    # time TIME NOT NULL,
    time = db.Column(db.Time, nullable=False)
    # image_link VARCHAR(500) NULL,
    image_link = db.Column(db.String(500), nullable=True)
    # description VARCHAR(255) NULL,
    description = db.Column(db.String(255), nullable=True)
    # author_id INT NOT NULL,
    author_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
    # tags TEXT[] NULL,
    tags = db.Column(db.ARRAY(db.String))
    # public BOOLEAN NOT NULL,
    public = db.Column(db.Boolean, nullable = False)
    # PRIMARY KEY (event_id),
    # FOREIGN KEY (author_id) REFERENCES app_user(user_id)
    location = db.Column(db.String(255), nullable = False)

    #relationshps
    attending_users = db.relationship('AppUser', secondary=participating_in, lazy='subquery',
        backref=db.backref('app_user', lazy=True))

#original method of making the participating table, not sure how to do it and it doesn't work but I left it just in case
# class Participants(db.Model):
#     __tablename__='participatingIn'
#     # user_id INT NOT NULL,
#     user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), primary_key=True)
#     # event_id INT NOT NULL,
#     event_id = db.Column(db.Integer, db.ForeignKey("event.event_id"), primary_key=True)
#     # PRIMARY KEY (user_id, event_id),
#     # FOREIGN KEY (user_id) REFERENCES app_user(user_id),
#     #I'm not entirely sure if this actually works but I'm trying it
#     user = db.relationship('AppUser', back_populates='app_user')
#     # FOREIGN KEY (event_id) REFERENCES event(event_id)
#     event = db.relationship('Event', back_populates='event')

#WIP
class Friends(db.Model):
    __tablename__='friends'
    # user1_id INT NOT NULL,
    user1_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'), primary_key=True)
    # user2_id INT NOT NULL,
    user2_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'), primary_key=True)
    # PRIMARY KEY (user1_id, user2_id),
    # FOREIGN KEY (user1_id) REFERENCES app_user(user_id),

    #I am not entirely sure if this is the correct way of setting up the foreign key relationships since they're both users
    #I found a lot of conflicting answers online on how to set them up but I chose to implement this one for now since it was closest to what we wanted
    #https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    user = db.relationship('AppUser', foreign_keys='Friends.user1_id')
    # FOREIGN KEY (user2_id) REFERENCES app_user(user_id)
    friend = db.relationship('AppUser', foreign_keys='Friends.user2_id')