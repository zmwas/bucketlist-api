from app import db
from .models import BucketList,BucketListItem
from app.users.models import User


def create_bucket_list(user_id,data):
    title = data.get('title')
    description = data.get('description')
    if len(title)==0 or title == None:
        return "Please provide a title for your bucketlist"
    bucketlists = BucketList.query.filter_by(user_id=user_id,title=title).first()
    if bucketlists is not None:
        return "Similar bucketlist title"
    bucketlist = BucketList(title=title,description=description,user_id=user_id)
    db.session.add(bucketlist)
    db.session.commit()

def get_bucketlist_by_name(user_id,title):
    bucketlist = BucketList.query.filter_by(user_id=user_id).filter(BucketList.title.ilike('%' + title + '%'))
    if len(bucketlist.all())==0:
        return "Bucketlist doesn't exist"
    return bucketlist

def get_all_bucketlists(user_id):
    user = User.query.get(user_id)
    bucketlists = user.bucketlists
    return bucketlists

def get_single_bucketlist(id,user_id):
    bucketlist = BucketList.query.filter_by(id=id,user_id=user_id).first()
    if bucketlist == None:
        return "Bucketlist doesn't exist"
    return bucketlist

def delete_bucket_list(id,user_id):
    bucketlist = get_single_bucketlist(id,user_id)
    if bucketlist == "Bucketlist doesn't exist":
        return "Bucketlist doesn't exist"
    db.session.delete(bucketlist)
    db.session.commit()

def update_bucket_list(id,user_id,data):
    title = data.get('title')
    description = data.get('description')
    bucketlist = get_single_bucketlist(id,user_id)
    if bucketlist == "Bucketlist doesn't exist":
        return "Bucketlist doesn't exist"
    bucketlist.title = title
    bucketlist.description = description
    db.session.add(bucketlist)
    db.session.commit()
    return bucketlist

def create_bucket_list_item(data,bucketlist_id,user_id):
    name = data.get('name')
    if name == None or len(name) == 0:
        return "Please provide a name for the item"
    item = BucketListItem(name=name)
    bucket_list = BucketList.query.\
                  filter_by(id=bucketlist_id,user_id=user_id).first()
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
