from datetime import datetime
from app.extensions import db
from app.extensions import logger
from sqlalchemy import (
    insert,
    update,
    delete,
    exc,
    func, 
    desc,
)
 

class BaseModel(db.Model):
    __abstract__ = True

    # @classmethod
    # def insert(cls, data):
    #     ''' data: list of dicts '''
    #     try:
    #         ids = db.session.scalars(insert(cls).returning(cls.id), data)
    #     except exc.SQLAlchemyError:
    #         ids = None
    #     return ids

    # @classmethod
    # def update(cls, data):
    #     try:
    #         ids = db.session.scalars(update(cls).returning(cls.id), data)
    #     except exc.SQLAlchemyError:
    #         ids = None
    #     return ids

    # @classmethod
    # def delete_bulk(cls, data):
    #     try:
    #         db.session.scalars(delete(cls), data)
    #         return True
    #     except exc.SQLAlchemyError:
    #         return False


    def save(self):
        ''' Save Entity '''
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            # add error to log
            return False

    def delete(self):
        ''' Delete Entity '''
        try:
            db.session.delete(self) 
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            # add error to log
            return False