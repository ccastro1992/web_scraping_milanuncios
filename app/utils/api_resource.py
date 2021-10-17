from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource, Api, reqparse


class ApiResource(Resource):
    def get(self):
        """
        ENDPOINT GET DEL MODELO ANUNCIO
        :filter GET title
        :filter GET description

        :return anuncios json:
        """
        model = self.MODEL_CLASS
        schema = self.SCHEMA_CLASS

        values = request.values
        title = values.get('title', False)
        description = values.get('description', False)

        try:
            if values:
                if title:
                    items = model.simple_filter(name=title)
                    many = False
                elif description:
                    items = model.simple_filter(description=description)
                    many = False
                else:
                    return jsonify({
                        'data': 'Parametro de busqueda incorrecto'
                    }), HTTPStatus.BAD_REQUEST
            else:
                items = model.get_all()
                many = True

        except Exception as e:
            return jsonify({
                'data': e
            }), HTTPStatus.BAD_REQUEST

        data = schema.dump(items, many=many)

        return jsonify({
            'data': data
        }), HTTPStatus.OK
