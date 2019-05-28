from backend.model.db import db



class Foodkey(db.Model):
    __tablename__ = 'elekey'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    e_type = db.Column(db.String(255))
    category = db.Column(db.String(255))
    e_category= db.Column(db.String(255))
    priority = db.Column(db.Integer)
    used = db.Column(db.Integer)
    hitted = db.Column(db.Integer)
    status = db.Column(db.Integer)
    maintainer = db.Column(db.Integer)
    datetime = db.Column(db.Integer)



    def __init__(self, id,name, type, e_type,category,e_category,priority,used,hitted,status,maintainer,datetime):

        self.id = id
        self.name = name
        self.type = type
        self.e_type = e_type
        self.category = category
        self.e_category = e_category
        self.priority = priority
        self.used = used
        self.hitted = hitted
        self.status = status
        self.maintainer = maintainer
        self.datetime = datetime

