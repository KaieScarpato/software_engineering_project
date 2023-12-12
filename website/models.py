from . import db

class Beer(db.Model):
    __tablename__ = 'beer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    brewer = db.Column(db.String(200))
    region = db.Column(db.String(50))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    tempBeerStyle1 = db.Column(db.String(200))
    tempBeerStyle2 = db.Column(db.String(200))
    primaryBeerStyle = db.Column(db.String(200))
    primaryBeerStyleDesc = db.Column(db.String(200))
    specificBeerStyle = db.Column(db.String(200))
    specificBeerStyleDesc = db.Column(db.String(500))
    foodPairing = db.Column(db.String(500))
    oz = db.Column(db.String(5))
    ml = db.Column(db.String(5))
    container = db.Column(db.String(20))
    abv = db.Column(db.String(5))
    ibu = db.Column(db.String(5))
    srm = db.Column(db.String(5))
    malt = db.Column(db.String(50))
    hops = db.Column(db.String(50))
    cals = db.Column(db.String(5))
    desc = db.Column(db.String(500))
    special = db.Column(db.Integer)
    searchFreq = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'user'
    role = db.Column(db.Integer)
    name = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(200))
    salt = db.Column(db.String(20))