from flask import jsonify, request, url_for
from flask.views import MethodView

from app import db
from app.schemas import PageSchema, PageCreateSchema, RevisionSchema, \
    RevisionsSchema, PageUpdateSchema
from .models import Revision, Page, Content


class APIListView(MethodView):
    def get(self):
        urls = (
            ('List all pages', url_for('page')),
            ('List all revisions of page', url_for('revisions', page_id=0)),
            ('Show page by revision',
             url_for('revisions', page_id=0, revision_id=0)),
            ('Current page (GET|POST)', (
                ('GET - get page by id', url_for('page', page_id=0)),
                ('POST - update page by id', url_for('page', page_id=0)),
            )),
            ('Set revision as current',
             url_for('revisions/set', page_id=0, revision_id=0))
        )

        return jsonify(urls)


class PageView(MethodView):
    schema_list = PageSchema
    schema_create = PageCreateSchema
    schema_update = PageUpdateSchema

    def post(self):
        form = request.form
        data, errors = self.schema_create().load(form)
        if errors:
            return jsonify(errors), 422

        page = Page.create_with_revision(data)
        res = self.schema_list().dump(page)
        return jsonify(res)

    def get(self, page_id):

        query = (
            db.session.query(Page.id,
                             Page.title,
                             Revision.actual,
                             Content.text)
            .join(Revision, Revision.page_id == Page.id)
            .join(Content, Revision.content_id == Content.id)
        )

        if page_id is None:
            pages = query.all()
            res, err = self.schema_list(many=True).dump(pages)
        else:
            page = query.filter(Page.id == page_id).first()
            res, err = self.schema_list().dump(page)

        if err:
            return jsonify(err), 422

        return jsonify(res)

    def put(self, page_id):
        form = request.form
        data, err = self.schema_update().load(form)
        if err:
            return jsonify(err), 422

        page = Page.query.get(page_id).update_with_revision(data)
        res = self.schema_list().dump(page)
        return jsonify(res)


class RevisionView(MethodView):
    schema_list = RevisionsSchema
    schema_single = RevisionSchema

    def get(self, page_id, revision_id):
        if not revision_id:
            # list all
            revisions = db.session.query(Revision).filter_by(
                page_id=page_id).all()
            res, err = self.schema_list(many=True).dump(revisions)
        else:
            # list single
            revision = (db.session.query(Revision.id, Revision.add_date,
                                         Revision.page_id, Revision.actual,
                                         Content.text, Page.title)
                        .join(Content, Content.id == Revision.content_id)
                        .join(Page, Page.id == Revision.page_id)
                        .filter(Revision.page_id == page_id)
                        .filter(Revision.id == revision_id)
                        .first()
                        )
            res, err = self.schema_single().dump(revision)

        if err:
            return jsonify(err), 422
        return jsonify(res)

    def post(self, page_id, revision_id):

        revision = Revision.query.get(revision_id).set_as_actual()
        res, err = self.schema_single().dump(revision)

        if err:
            return jsonify(err), 422
        return jsonify(res)
