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
