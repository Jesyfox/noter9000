import os
import urllib.parse as urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from .utils import get_date, correct_
from .db_bridge import DataBaseHandler


class Noter(object):

    def __init__(self, host, port):
        self.data_base = DataBaseHandler(host=host,
                                         port=port,
                                         db_name='notes_db',
                                         col_name='notes')
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='my_notes'),
            Rule('/note', endpoint='new_note'),
            Rule('/clear_notes', endpoint='clear_notes')
        ])

    def render_template(self, html_template_name, **context):
        """Take html file_template from templates folder and render it for browser"""
        template = self.jinja_env.get_template(html_template_name)
        return Response(template.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        """takes on_(endpoint) attribute from request url
           returning self.function that matches with on_(endpoint)"""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def on_new_note(self, request):
        error = None
        note = {}
        if request.method == 'POST':
            note = {'title': request.form['title'],
                    'description': request.form['description'],
                    'date_created': get_date()
                    }

            print('header:', note)
            if not correct_(note):
                error = 'you must fill inputs!'
            else:
                self.data_base.new_note(note)
                return redirect('/')
        return self.render_template('new_note.html',
                                    error=error,
                                    note=note)

    def on_my_notes(self, request):
        return self.render_template('my_notes.html',
                                    notes=self.data_base.get_notes())

    def on_clear_notes(self, request):
        self.data_base.kill()
        return redirect('/')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

