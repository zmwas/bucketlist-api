from app import db
from models import BucketList


def create_bucket_list(data):
    title = data.get('title')
    description = data.get('description')
    bucketlist = BucketList(title=title,description=description)
    db.session.add(bucketlist)
    db.session.commit()

def get_all_bucketlists():
    return BucketList.query.all()

def get_single_bucketlist(id):

    bucketlist = BucketList.query.filter_by(id=id).first()
    if bucketlist == None:
        return "Bucketlist doesn't exist"
    return bucketlist

def delete_bucket_list(id):
    bucketlist = BucketList.query.get(id)
    if bucketlist == None:
        return "Bucketlist doesn't exist"
    db.session.delete(bucketlist)
    db.session.commit()
