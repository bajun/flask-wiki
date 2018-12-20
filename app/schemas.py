from flask_marshmallow.fields import Hyperlinks, URLFor
from marshmallow import Schema, fields, validates, ValidationError
from app import db, Page


class PageCreateSchema(Schema):
    title = fields.String()
    content = fields.String()

    @validates('title')
    def validate_title(self, value):
        page = db.session.query(Page).filter_by(title=value).first()
        if page:
            raise ValidationError('Page with such title already exists')


class PageUpdateSchema(Schema):
    content = fields.String()


class PageSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    text = fields.String()
    actual = fields.Integer()

    _links = Hyperlinks({
        'self': URLFor('page', page_id='<id>'),
        'collection': URLFor('page'),
        'revisions': URLFor('revisions', page_id='<id>')
    })


class RevisionsSchema(Schema):
    id = fields.Integer()
    actual = fields.Integer()
    url = URLFor('revisions', page_id='<page_id>', revision_id='<id>')


class RevisionSchema(Schema):
    id = fields.Integer()
    add_date = fields.DateTime()
    title = fields.String()
    text = fields.String()
    actual = fields.Boolean()

    _links = Hyperlinks({
        'self': URLFor('revisions', page_id='<page_id>', revision_id='<id>'),
        'make-actual': URLFor('revisions/set', page_id='<page_id>',
                              revision_id='<id>'),
        'page-revisions': URLFor('revisions', page_id='<id>')
    })
