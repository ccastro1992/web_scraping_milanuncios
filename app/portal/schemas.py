from app.utils.ma import ma
from marshmallow_sqlalchemy import fields

from .models import Category, SubCategory, Advertisement


class AdvertisementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advertisement
        load_instance = True
        include_fk = True


class SubCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubCategory
        load_instance = True


class CategorySchema(ma.SQLAlchemyAutoSchema):
    subcategories = fields.Nested(SubCategorySchema, many=True)

    class Meta:
        model = Category
        load_instance = True
