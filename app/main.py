import os
import urllib.parse as urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from .noter import Noter


def create_app(with_static=True):
    app = Noter()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


def main():
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app,
               use_debugger=True,
               use_reloader=True)


if __name__ == '__main__':
    main()
