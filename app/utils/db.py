from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModelMixin:
    def save(self):
        """
        Almacena un nuevo registro en bdd
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Elimina un registro en bdd
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
        Obtiene todos los registros de la bdd
        :return records:
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un registro de la bdd mediante el id
        :param id (int):
        :return record:
        """
        return cls.query.get(id)

    @classmethod
    def simple_filter(cls, **kwargs):
        """
        Obtiene un registro filtrado por el argumento enviado
        :param kwargs: parametros de filtro
        :return record:
        """
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_by_name(cls, name):
        """
        Obtiene un registro filtrado por el argumento enviado
        :param name: nombre del registro
        :return record:
        """
        return cls.query.filter_by(name=name).first()
