from sqlalchemy import Column, Integer, String, Float

class Repository:
    def __init__(self, db, planet, user, 
                 planet_schema, user_schema, jwt):
        self.db = db
        self.planet = planet
        self.planet_schema = planet_schema()
        self.planets_schema = planet_schema(many=True)
        self.user = user
        self.user_schema = user_schema()
        self.users_schema = user_schema(many=True)
        self.jwt = jwt

def register_repository(db, schema, jwt):
    # Model
    class User(db.Model):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        first_name = Column(String)
        last_name = Column(String)
        email = Column(String, unique=True)
        password = Column(String)

    class Planet(db.Model):
        __tablename__ = 'planets'
        planet_id = Column(Integer, primary_key=True)
        planet_name = Column(String)
        planet_type = Column(String)
        home_star = Column(String)
        mass = Column(Float)
        radius = Column(Float)
        distance = Column(Float)
    
    # Schema
    class UserSchema(schema.Schema):
        class Meta:
            fields = ('id', 'first_name', 'last_name', 'email', 'password')


    class PlanetSchema(schema.Schema):
        class Meta:
            fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

    return Repository(db, Planet, User, PlanetSchema, UserSchema, jwt)
