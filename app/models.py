import werkzeug
from app import db
from flask_login import UserMixin

#relationship that allows a user to save a race
#a user can save many races and a race can be saved by many users
user_race = db.Table('user_race',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('race_id', db.Integer, db.ForeignKey('race.id'), primary_key=True)
)

#relationship that allows a user to save a competitor
#a user can save many competitors and a competitor can be saved by many users
user_competitor = db.Table('user_competitor',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('competitor_id', db.Integer, db.ForeignKey('competitor.id'), primary_key=True)
)

#table to create a many-to-many relationship between races and competitors 
#a competitor can have many races and a race has many competitors
class CompetitorRace(db.Model):
    __tablename__= 'competitor_races'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'), nullable=False) #Foreign key from competitor table
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'), nullable=False) #Foreign key from race table
    result = db.Column(db.String(10)) #stores the result for a competitor in a specific race

    competitor = db.relationship('Competitor', back_populates='competitor_races')
    race = db.relationship('Race', back_populates='competitor_races')

class Competitor(db.Model):
    __tablename__ ='competitor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), index=True, unique=True)
    last_name = db.Column(db.String(25), index=True, unique=True)
    club = db.Column(db.String(100))
    age = db.Column(db.Integer)
    competitor_races = db.relationship('CompetitorRace', back_populates='competitor')

class Race(db.Model):
    __tablename__= 'race'
    id = db.Column(db.Integer, primary_key=True)
    race_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.Boolean, default=False) # true for complete, false for incomplete
    competitor_races = db.relationship('CompetitorRace', back_populates='race')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    saved_races = db.relationship('Race', secondary=user_race, backref='saved_by_users')
    saved_competitors = db.relationship('Competitor', secondary=user_competitor, backref='saved_by_users')
    is_admin = db.Column(db.Boolean, default=False) #allows for admin accessibility 

    def __repr__(self):
        return f'<User {self.username}>'
    
    def check_password(self, password):
        #hash password for security
        werkzeug.security.generate_password_hash 
        return self.password == password