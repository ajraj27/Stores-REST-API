
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('price',
    type=float,required=True,
    help="This Field cannot be left blank")

    parser.add_argument('store_id',
    type=int,required=True,
    help="Every item needs a store_id")

    @jwt_required()
    def get(self,name):
        item=ItemModel.get_by_name(name)

        if(item):
            return item.json()
        return {'message':'Item not found'},404

    def post(self,name):
        if ItemModel.get_by_name(name):
            return {'message':"An item with name '{}' already exists".format(name)},400

        data=Item.parser.parse_args()

        item=ItemModel(name,**data)

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured in creating this item.'},500    # Internal Server Error

        return item.json(),201

    def delete(self,name):
        item=ItemModel.get_by_name(name)

        if(item):
            item.delete_from_db()

        return {'message':'Item deleted'}


    def put(self,name):

        data=Item.parser.parse_args()

        item=ItemModel.get_by_name(name)

        if item is None:
            item=ItemModel(name,**data)
        else:
            item.price=data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
