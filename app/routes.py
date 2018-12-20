from app import application, APIListView, PageView, RevisionView

list_all_api = APIListView.as_view('api')
application.add_url_rule('/api/', view_func=list_all_api, methods=['GET', ])

page_api = PageView.as_view('page')
application.add_url_rule('/api/page/', view_func=page_api, methods=['POST', ])
application.add_url_rule('/api/page/', view_func=page_api, methods=['GET', ],
                         defaults={'page_id': None})
application.add_url_rule('/api/page/<int:page_id>/', view_func=page_api,
                         methods=['GET'])
application.add_url_rule('/api/page/<int:page_id>/', view_func=page_api,
                         methods=['PUT'])

revision_api = RevisionView.as_view('revisions')

application.add_url_rule(
    '/api/page/<int:page_id>/revisions/<int:revision_id>/',
    view_func=revision_api,
    methods=['GET', ])

application.add_url_rule(
    '/api/page/<int:page_id>/revisions/<int:revision_id>/actual/',
    view_func=revision_api,
    methods=['POST', ], endpoint='revisions/set')

application.add_url_rule('/api/page/<int:page_id>/revisions/',
                         view_func=revision_api, methods=['GET', ],
                         defaults={'revision_id': None})
