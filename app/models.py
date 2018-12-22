from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, \
    DateTime, MetaData
from sqlalchemy.orm import relationship

from app import db

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


class Page(db.Model):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, unique=True)
    revision_latest = Column(String)

    revision = relationship("Revision", backref="page",
                            foreign_keys="Revision.page_id",
                            cascade="all,delete")

    def __repr__(self):
        return '<{}>'.format(self.title)

    @staticmethod
    def create_with_revision(data):
        page = Page(title=data.get('title'))
        content = Content(text=data.get('content'))
        revision = Revision(page=page, content=content, actual=True)

        db.session.add(revision)
        db.session.commit()

        page.set_latest_revision(revision)
        content.add_revision(revision)

        return {
            'id': page.id,
            'title': page.title,
            'actual': revision.id,
            'content': content.text
        }

    def update_with_revision(self, data):
        content = Content(text=data.get('content'))
        revision = Revision(page=self, content=content, actual=True)

        db.session.add(revision)
        db.session.commit()

        revision.set_as_actual()
        content.add_revision(revision)

        return {
            'id': self.id,
            'title': self.title,
            'actual': revision.id,
            'content': content.text
        }

    def set_latest_revision(self, revision):
        self.revision_latest = revision.id
        db.session.add(self)
        db.session.commit()


class Content(db.Model):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)
    revision_id = Column(Integer, ForeignKey('revision.id', use_alter=True,
                                             name='revision_fk'))
    revision = relationship("Revision", backref="content",
                            foreign_keys="Revision.content_id")

    def add_revision(self, revision):
        self.revision_id = revision.id
        db.session.add(self)
        db.session.commit()


class Revision(db.Model):
    __tablename__ = 'revision'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer,
                     ForeignKey('page.id', use_alter=True, name='page_fk'))
    content_id = Column(Integer, ForeignKey('content.id', use_alter=True,
                                            name='content_fk'))
    actual = Column(Boolean)
    add_date = Column(DateTime,
                      nullable=False,
                      default=datetime.utcnow
                      )

    def set_as_actual(self):
        db.session.query(Revision).filter_by(page_id=self.page_id).update(
            {'actual': False})
        self.actual = True
        db.session.add(self)
        db.session.commit()

        return {
            'id': self.id,
            'add_date': self.add_date,
            'page_id': self.page_id,
            'actual': self.actual,
            'text': self.content.text,
            'title': self.page.title
        }
