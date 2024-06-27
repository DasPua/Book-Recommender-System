from flask_mongoengine import MongoEngine

db = MongoEngine()

class Listing(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    image = db.StringField()
    writer = db.StringField(required=True)
    price = db.IntField(required=True)

class Review(db.Document):
    content = db.StringField(required=True)
    rating = db.IntField(required=True)
    listing = db.ReferenceField(Listing, reverse_delete_rule=db.CASCADE)
