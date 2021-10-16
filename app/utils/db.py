from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModelMixin:
    def save(self):
        """

        :return:
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """

        :return:
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all(cls):
        """

        :return:
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """

        :param id:
        :return:
        """
        return cls.query.get(id)

    @classmethod
    def simple_filter(cls, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_by_name(cls, name):
        """

        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()
