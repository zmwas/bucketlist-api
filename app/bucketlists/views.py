from flask import g,request
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import NotFound,Unauthorized,BadRequest
from flask_restplus import Resource
from flask_restplus import reqparse

from app.utils import api
from .serializers import bucketlist,bucketlist_item
from .controller import (create_bucket_list,get_all_bucketlists,
                       get_single_bucketlist,delete_bucket_list,
                       get_single_bucketlist_item,get_bucketlist_by_name,
                       update_bucket_list,create_bucket_list_item,
                       update_bucket_list_item,delete_bucket_list_items)
from app.users.models import User
from .models import BucketList,BucketListItem

token_auth = HTTPTokenAuth('Bearer')

namespace = api.namespace('bucketlist',description='BucketList operations')



@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user or type(user)!= User:
        raise Unauthorized("Not Authorized")
        return False
    g.user = user
    return True



@namespace.route('/')
class BucketListResource(Resource):
    @api.marshal_list_with(bucketlist)
    @token_auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q',required=False,location='args')
        parser.add_argument('page',type=int, required=False,
         default=1, help='Page number',location='args')
        parser.add_argument('per_page', type=int, required=False,
                            choices=[2, 10, 20, 30, 40, 50],
                            default=10,
                            help='Results per page {error_msg}',location='args')
        args = parser.parse_args()
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        if args["q"]:
            print (args)
            bucket_name = args.get('q')
            if get_bucketlist_by_name(g.user.id,bucket_name) == "Bucketlist doesn't exist":
                raise NotFound("Bucketlist doesn't exist")
            return get_bucketlist_by_name(g.user.id,bucket_name).all()
        elif args['page'] and args['per_page']:
            return get_all_bucketlists(g.user.id).paginate(page, per_page, error_out=False).items
        elif args['page'] and args['per_page'] and args['q']:
            return get_bucketlist_by_name(g.user.id,bucket_name).paginate(page, per_page, error_out=False).items




    @api.expect(bucketlist)
    @token_auth.login_required
    def post(self):
        """
        Creates new bucketlist

        """
        data = request.get_json(force = True)
        title = data.get('title')
        title  = title.strip()
        if title == None or len(title)==0:
            raise BadRequest("Please provide a title for your bucketlist")
        bucketlists = BucketList.query.filter_by(user_id=g.user.id,title=title).first()
        if bucketlists is not None:
            raise BadRequest("A bucketlist with that name exists")
        create_bucket_list(g.user.id,data)
        return  200


@namespace.route('/<int:id>')
@namespace.param('id','BucketList identifier')
class SingleBucketListResource(Resource):
    @token_auth.login_required
    @api.marshal_with(bucketlist)
    def get(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        return get_single_bucketlist(id,g.user.id)
    @token_auth.login_required
    def delete(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        return delete_bucket_list(id,g.user.id), 200
    @token_auth.login_required
    @api.expect(bucketlist)
    def put(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        data = request.get_json(force = True)
        update_bucket_list(id,g.user.id,data)
        return 200

@namespace.route('/<int:id>/items')
@namespace.param('id','BucketList identifier')
class BucketListItemsResource(Resource):
    @token_auth.login_required
    @api.expect(bucketlist_item)
    def post(self,id):
        data = request.get_json(force = True)
        name  = data.get('name').strip()
        item = BucketListItem.query.filter_by(bucketlist_id=id,name=name).first()
        if name == None or len(name) == 0:
            raise BadRequest("Please provide a name for the item")
        elif get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif item is not None:
            raise BadRequest("Please provide a name for the item")
        create_bucket_list_item(data,id,g.user.id)
        return 200


@namespace.route('/<int:id>/items/<int:item_id>')
@namespace.param(('id','BucketList identifier'),('item_id','BucketListItem identifier'))
class BucketListItemsResource(Resource):
    @token_auth.login_required
    @api.expect(bucketlist_item)
    def put(self,id,item_id):
        data = request.get_json(force = True)
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        update_bucket_list_item(id,item_id,data)
        return 200
    @token_auth.login_required
    def delete(self,id,item_id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        return delete_bucket_list_items(id,item_id),200
