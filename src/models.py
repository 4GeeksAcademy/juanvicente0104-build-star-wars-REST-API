from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", uselist=True, backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": list(map(lambda item: item.serialize(),self.favorites))
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    # __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
#    eye_color = db.Column(db.String(20), unique=True, nullable=False)
    height = db.Column(db.Integer, nullable=False, unique=False)
    mass = db.Column(db.Integer,nullable=False,unique=False)
    gender = db.Column(db.String(10),nullable=False,unique=False)
    favorites = db.relationship("Favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender
        }
    

class Planets(db.Model):
    # __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
 ##   population = db.Column(db.Integer, unique=True, nullable=False)
    climate = db.Column(db.String(20), unique=False, nullable=False)
    terrain = db.Column(db.String(20), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    favorites = db.relationship("Favorites")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

class Favorites(db.Model):
    # __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer,db.ForeignKey("people.id"))
    planets_id = db.Column(db.Integer,db.ForeignKey("planets.id"))

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.people_id,
            "planets_id": self.planets_id 
        }