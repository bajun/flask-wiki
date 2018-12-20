from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, \
    DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app import db


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
            'text': content.text
        }

    def update_with_revision(self, data):
        content = Content(text=data.get('content'))
        revision = Revision(page=self, content=content, actual=True)

        db.session.add(revision)
        db.session.commit()

        self.set_latest_revision(revision)
        content.add_revision(revision)

        return {
            'id': self.id,
            'title': self.title,
            'actual': revision.id,
            'text': content.text
        }

    def set_latest_revision(self, revision):
        self.revision_latest = revision.id
        db.session.add(self)
        db.session.commit()


class Content(db.Model):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)
    revision_id = Column(Integer, ForeignKey('revision.id'))
    revision = relationship("Revision", backref="content",
                            foreign_keys="Revision.content_id",
                            cascade="all,delete")

    def add_revision(self, revision):
        self.revision_id = revision.id
        db.session.add(self)
        db.session.commit()


class Revision(db.Model):
    __tablename__ = 'revision'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('page.id'))
    content_id = Column(Integer, ForeignKey('content.id'))
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
