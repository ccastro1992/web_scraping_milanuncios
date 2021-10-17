import logging

import requests
from flask import render_template, jsonify
from flask import request
from http import HTTPStatus
from ..utils.scraping import Scraping
from . import portal_bp
from .forms import ScrapingForm
from .models import Category, SubCategory
from .schemas import CategorySchema, SubCategorySchema
from flask_login import login_required

logger = logging.getLogger(__name__)


@portal_bp.route("/")
@login_required
def index():
    """
    Inicializa el formulario del portal y renderiza la plantilla index
    :return:
    """
    form = ScrapingForm()
    error = None
    return render_template("index.html", form=form, error=error)


@portal_bp.route("/start_scraping", methods=['POST'])
@login_required
def start_scraping():
    """
    Consulta el sitio web y obtiene las categorias para almacenar en bdd
    :return json categorias:
    """
    category_schema = CategorySchema()

    web_scraping = Scraping('https://www.milanuncios.com')
    categories = web_scraping.get_categories()

    for category in categories:
        #advertisements = web_scraping.get_advertisements([category])

        old_category = Category.get_by_name(category.get('name'))
        if old_category is None:
            category_obj = Category(
                name=category.get('name'),
                url=category.get('url')
            )
            category_obj.save()
            for subcategory in category.get('sub_categories', []):
                old_subcategory = SubCategory.get_by_name(subcategory.get('name'))
                if old_subcategory is None:
                    subcategory_obj = SubCategory(
                        name=subcategory.get('name'),
                        url=subcategory.get('url'),
                        category_id=category_obj.id
                    )
                    subcategory_obj.save()

    items = Category.get_all()
    data = category_schema.dump(items, many=True)

    return jsonify({
        'data': data
    }), HTTPStatus.OK


@portal_bp.route("/get_subcategory", methods=['POST'])
@login_required
def get_subcategory():
    """
    Obtiene las subcategorias para almacenar en bdd
    :return json subcategorias:
    """
    category_schema = SubCategorySchema()
    category_id = int(request.values.get('category_id'))
    items = SubCategory.simple_filter(category_id=category_id)
    data = category_schema.dump(items, many=True)

    return jsonify({
        'data': data
    }), HTTPStatus.OK
