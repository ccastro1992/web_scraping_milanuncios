from app.utils.db import db, BaseModelMixin


class Category(db.Model, BaseModelMixin):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=True)
    subcategories = db.relationship('SubCategory', backref='subcategory', lazy='dynamic')


class SubCategory(db.Model, BaseModelMixin):
    __tablename__ = 'subcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Advertisement(db.Model, BaseModelMixin):
    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
