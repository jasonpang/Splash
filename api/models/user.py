from mongoengine import Document, StringField, ListField


class User(Document):
    name = StringField()
    phone = StringField()
    email = StringField()
    password = StringField()
    salt = StringField()
    picture_profile = StringField()
    picture_thumbnail = StringField()
    quote = StringField()
    school = StringField()
    year = StringField()
    major = StringField()
    company = StringField()
    title = StringField()
    location = StringField()
    interests = StringField()
    skills = StringField()
    profile = StringField()
    contacts = ListField()