from mongoengine import Document, StringField, ListField


class User(Document):
    name = StringField()
    phone = StringField()
    email = StringField()
    password = StringField()
    salt = StringField()
    picture_profile = StringField()
    picture_thumbnail = StringField()
    description = StringField()
    education = StringField()
    employer = StringField()
    interests = StringField()
    skills = StringField()
    contacts = ListField()