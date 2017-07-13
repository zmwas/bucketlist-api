from app import db




class BucketList(db.Model):
    __tablename__ = "bucketlists"

    id  = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25),unique=True)
    description = db.Column(db.String(250),unique=False)
