import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from console.cli import register_cli
from repository import register_repository


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

repository = register_repository(SQLAlchemy(app), 
                                 Marshmallow(app), 
                                 JWTManager(app))
register_cli(app, repository)

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = repository.planet.query.all()
    result = repository.planets_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = repository.user.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = repository.user(first_name=first_name, last_name=last_name, email=email, password=password)
        repository.db.session.add(user)
        repository.db.session.commit()
        return jsonify(message="User created successfully."), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = repository.user.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401





@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = repository.planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = repository.planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    test = repository.planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify("There is already a planet by that name"), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = repository.planet(planet_name=planet_name,
                                       planet_type=planet_type,
                                       home_star=home_star,
                                       mass=mass,
                                       radius=radius,
                                       distance=distance)

        repository.db.session.add(new_planet)
        repository.db.session.commit()
        return jsonify(message="You added a planet"), 201


@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = repository.planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        repository.db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
