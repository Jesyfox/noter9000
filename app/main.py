import os
import urllib.parse as urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from .noter import Noter
from .server_settings import HOST, PORT, MONGO_HOST, MONGO_PORT


def create_app(host, port,with_static=True):
    app = Noter(host, port)
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


def main():
    from werkzeug.serving import run_simple
    app = create_app(host=MONGO_HOST,
                     port=MONGO_PORT)
    run_simple(HOST, PORT, app,
               use_debugger=True,
               use_reloader=True)


if __name__ == '__main__':
    main()
