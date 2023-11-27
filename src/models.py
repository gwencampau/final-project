from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AppUser(db.Model):
    __tablename__ = 'app_user'
    # user_id SERIAL,
    user_id = db.Column(db.Integer, primary_key=True) # Not sure how to do serial stuff
    # username VARCHAR(20) NOT NULL,
    username = db.Column(db.String(20), nullable=False)
    # password VARCHAR(255) NOT NULL,
    password = db.Column(db.String(255), nullable=False)
    # profile_img bytea NULL,
    profile_img = db.Column(db.String(100), nullable=True) # Having issues with the BYTEA thing here
    # bio VARCHAR(150) NULL,
    bio = db.Column(db.String(150), nullable=True)
    # PRIMARY KEY (user_id)
