from flask import request
from flask_restful import Resource
from app.utils.error_handling import ItemNotFound
from app.utils.response_json import response_json
from http import HTTPStatus


class ApiResource(Resource):
    def get(self, id=None):
        model = self.MODEL_CLASS
        schema = self.SCHEMA_CLASS

        if not id:
            items = model.get_all()
            many = True
        else:
            items = model.query.get(id)
            many = False

        if not items:
            raise ItemNotFound('No Data!')

        data = schema.dump(items, many=many)

        return response_json(data=data, code=HTTPStatus.OK)

    def post(self):
        model = self.MODEL_CLASS
        schema = self.SCHEMA_CLASS

        data = request.get_json()
        new_item = schema.load(data)
        new_item.save()
        data = schema.dump(new_item)

        return response_json(data=data, code=HTTPStatus.CREATED)

    def put(self, id=None):
        model = self.MODEL_CLASS
        schema = self.SCHEMA_CLASS

        data_json = request.get_json()

        item = model.query.get(id)
        if item:
            for key in data_json.keys():
                if hasattr(item, key):
                    setattr(item, key, data_json.get(key))
                else:
                    raise ItemNotFound("Not found attribute ({})".format(key))
            item.save()
            data = schema.dump(item, many=False)
        else:
            raise ItemNotFound('Not found !')

        return response_json(data=data, code=HTTPStatus.OK)

    def delete(self, id=None):
        model = self.MODEL_CLASS

        item = model.query.get(id)
        if item:
            item.delete()
        else:
            raise ItemNotFound('Not found !')

        msg = "Item delete ({})".format(id)
        return response_json(code=HTTPStatus.OK, message=msg)
