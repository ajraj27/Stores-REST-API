
from db import db

class StoreModel(db.Model):
    __tablename__='stores'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))

    def __init__(self,name):
        self.name=name

    items=db.relationship('ItemModel',lazy='dynamic')

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]}

    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  #SELECT * FROM __tablename__ WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
