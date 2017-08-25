from app import db



class BucketList(db.Model):
    """
    Model for bucket list table
    """
    __tablename__ = "bucketlists"

    id  = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.String(250),unique=False)
    bucketlistitems = db.relationship('BucketListItem',backref='bucketlist'\
                                      ,lazy='dynamic'\
                                      ,cascade="all, delete-orphan")
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class BucketListItem(db.Model):
    """
    Model for bucket list item table
    """
    __tablename__ = "bucketlistitems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    bucketlist_id = db.Column(db.Integer,db.ForeignKey('bucketlists.id'))
