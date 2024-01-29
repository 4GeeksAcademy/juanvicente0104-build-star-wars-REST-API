"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people',methods=['GET']) #Get all the characters
def get_characters():
    characters = People.query.all()
    characters_serialized = [character.serialize() for character in characters]
    return jsonify(characters_serialized), 200

@app.route('/people/<int:people_id>') #Get character by id
def get_character_by_id(people_id):
    character = People.query.get(people_id)

    if character is None:
        return jsonify({"msg":"Character does not exist"}), 404

    character_serialized = character.serialize()
    return jsonify(character_serialized), 200

@app.route('/planets',methods=['GET']) #Get all the planets
def get_planets():
    planets = Planets.query.all()
    planets_serialized = [planet.serialize() for planet in planets]
    return jsonify(planets_serialized), 200

@app.route('/planets/<int:planet_id>', methods=['GET']) #Get planet by id
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"msg":"The planet does not exists"}), 404

    planet_serialized = planet.serialize()
    return jsonify(planet_serialized), 200

@app.route('/users', methods=['GET']) #Get all the users
def get_users():
    users = User.query.all() #Class User is really a db with all the User
    users_serialized = [user.serialize() for user in users]
    return jsonify(users_serialized), 200

@app.route('/favorite/planet/<int:planet_number>/<int:user_number>', methods=['POST']) #Add a new planet favorite to a specific user
def create_planet_favorite_by_ids(planet_number,user_number):
    favorite = Favorites.query.filter_by(user_id = user_number, planets_id = planet_number).first() #search

    if favorite is not None:
        return jsonify({"msg":"This favorite already exists"}), 400

    new_favorite = Favorites(user_id = user_number, planets_id = planet_number) #instanciamos la clase
    db.session.add(new_favorite)

    try:
        db.session.commit()
        return jsonify({"msg":"The favorite was added"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":f"{error}"}), 500

@app.route('/users/favorites/<int:user_number>',methods=['GET']) #Get all the favorites that belong to the user with user_id = user_number
def get_favorites_by_user(user_number):
    user = User.query.get(user_number)

    if user is None:
        return jsonify({"msg":"The user does not exists"}), 404

    user_serialized = user.serialize()
    return jsonify(user_serialized)

@app.route('/favorite/people/<int:people_number>/<int:user_number>',methods=['POST']) #Add a new character favorite to a specific user
def create_character_favorite_by_ids(people_number,user_number):
    favorite = Favorites.query.filter_by(user_id = user_number, people_id = people_number).first() #search

    if favorite is not None:
        return jsonify({"msg":"This favorite already exists"}), 400

    new_favorite = Favorites(user_id = user_number, people_id = people_number)
    db.session.add(new_favorite)

    try:
        db.session.commit()
        return jsonify({"msg":"The favorite was added"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":f"{error}"}), 500

@app.route('/favorite/planet/<int:planet_number>/<int:user_number>',methods=['DELETE'])  
def delete_planet_favorite_by_ids(planet_number,user_number):
    favorite = Favorites.query.filter_by(user_id = user_number, planets_id = planet_number).first()

    if favorite is None:
        return jsonify({"msg":"This favorite does not exist"}), 404

    try:
        db.session.delete(favorite)  
        db.session.commit()
        return jsonify({"msg":"The favorite was deleted"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":f"{error}"}), 500

@app.route('/favorite/people/<int:people_number>/<int:user_number>',methods=['DELETE'])
def delete_character_favorite_by_ids(people_number,user_number):
    favorite = Favorites.query.filter_by(user_id = user_number, people_id = people_number).first()

    if favorite is None:
        return jsonify({"msg":"This favorite does not exist"}), 404

    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg":"The favorite was deleted"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg":f"{error}"}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
