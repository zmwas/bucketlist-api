from flask import g,request,make_response,jsonify
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import NotFound,Unauthorized,BadRequest
from flask_restplus import Resource
from flask_restplus import reqparse

from app.utils import api
from serializers import bucketlist,bucketlistitems,bucket
from controller import (create_bucket_list,get_all_bucketlists,
                       get_single_bucketlist,delete_bucket_list,
                       get_single_bucketlist_item,get_bucketlist_by_name,
                       update_bucket_list,create_bucket_list_item,
                       update_bucket_list_item,delete_bucket_list_items)
from app.users.models import User
from models import BucketList,BucketListItem

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
    @api.header('Authorization', type=str, required=True)
    @api.marshal_list_with(bucketlist)
    @token_auth.login_required
    def get(self):
        """
        Get all bucketlists

        """
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
            bucket_name = args.get('q')
            if get_bucketlist_by_name(g.user.id,bucket_name) == "Bucketlist doesn't exist":
                raise NotFound("Bucketlist doesn't exist")
            return get_bucketlist_by_name(g.user.id,bucket_name).all()
        elif args['page'] and args['per_page']:
            return get_all_bucketlists(g.user.id).paginate(page, per_page, error_out=False).items
        elif args['page'] and args['per_page'] and args['q']:
            return get_bucketlist_by_name(g.user.id,bucket_name).paginate(page, per_page, error_out=False).items

        return  get_all_bucketlists(g.user.id).paginate(page, per_page, error_out=False).items


    @api.header('Authorization', type=str, required=True)
    @api.expect(bucketlist)
    @token_auth.login_required
    def post(self):
        """
        Create new bucketlist

        """
        data = request.get_json(force = True)
        title = data.get('title')
        if title.strip() == None or len(title.strip())==0:
            raise BadRequest("Please provide a title for your bucketlist")
        bucketlists = BucketList.query.filter_by(user_id=g.user.id,title=title).first()
        if bucketlists is not None:
            raise BadRequest("A bucketlist with that name exists")
        create_bucket_list(g.user.id,data)
        return {"message":"BucketList successfully created"}, 201


@namespace.route('/<int:id>')
class SingleBucketListResource(Resource):
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    @api.marshal_with(bucketlist)
    def get(self,id):
        """
        Get a single bucketlist

        """
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        return get_single_bucketlist(id,g.user.id)
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    def delete(self,id):
        """
        Delete a single bucketlist

        """

        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        delete_bucket_list(id,g.user.id)
        return ({"message":"BucketList successfully deleted"},200)
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    @api.expect(bucketlist)
    def put(self,id):
        """
        Update a single bucketlist

        """
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        data = request.get_json(force = True)
        update_bucket_list(id,g.user.id,data)
        return {"message":"BucketList successfully updated"},200

@namespace.route('/<int:id>/items')
class BucketListItemsResource(Resource):
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    @api.expect(bucketlistitems)
    def post(self,id):
        """
        Create a  bucketlist item

        """
        data = request.get_json(force = True)
        name  = data.get('name')
        item = BucketListItem.query.filter_by(bucketlist_id=id,name=name).first()
        if name.strip() == None or len(name.strip()) == 0:
            raise BadRequest("Please provide a name for the item")
        elif get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif item is not None:
            raise BadRequest("Item with that name exists")
        create_bucket_list_item(data,id,g.user.id)
        return {"message":"BucketList item successfully created"},201


@namespace.route('/<int:id>/items/<int:item_id>')
class BucketListItemsResource(Resource):
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    @api.expect(bucketlistitems)
    def put(self,id,item_id):
        """
        Update a  bucketlist item

        """

        data = request.get_json(force = True)
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        update_bucket_list_item(id,item_id,data)
        return {"message":"BucketList item successfully updated"},200
    @api.header('Authorization', type=str, required=True)
    @token_auth.login_required
    def delete(self,id,item_id):
        """
        Delete a  bucketlist item

        """
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
            delete_bucket_list_items(id,item_id)
        return ({"message":"BucketList item successfully deleted"},200)
