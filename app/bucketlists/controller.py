from app import db
from models import BucketList,BucketListItem


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
    bucketlist = get_single_bucketlist(id)
    if bucketlist == "Bucketlist doesn't exist":
        return "Bucketlist doesn't exist"
    db.session.delete(bucketlist)
    db.session.commit()

def update_bucket_list(id,data):
    title = data.get('title')
    description = data.get('description')
    bucketlist = get_single_bucketlist(id)
    if bucketlist == "Bucketlist doesn't exist":
        return "Bucketlist doesn't exist"
    bucketlist.title = title
    bucketlist.description = description
    db.session.add(bucketlist)
    db.session.commit()
    return bucketlist


def create_bucket_list_item(data,bucketlist_id):
    name = data.get('name')
    item = BucketListItem(name=name)
    bucket_list = BucketList.query.filter_by(id=bucketlist_id).first()
    bucket_list.bucketlistitems.append(item)
    db.session.add(item)
    db.session.commit()

def get_single_bucketlist_item(id,item_id):
    item = BucketListItem.query.filter_by(id=item_id,bucketlist_id=id).first()
    if item == None:
        return "Item doesn't exist"
    return item


def update_bucket_list_item(id,item_id,data):
    name = data.get('name')
    item = get_single_bucketlist_item(id,item_id)
    if item == "Item doesn't exist":
        return "Item doesn't exist"
    item.name = name
    db.session.add(item)
    db.session.commit()
def delete_bucket_list_items(id,item_id):
    item = get_single_bucketlist_item(id,item_id)
    if item == "Item doesn't exist":
        return "Item doesn't exist"
    db.session.delete(item)
    db.session.commit()
