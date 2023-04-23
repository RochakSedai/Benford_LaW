from pyramid.config import Configurator
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    with Configurator() as config:
        # config.add_route('benford', '/benford')
        config.include('urls')
        config.add_static_view(name='static', path='static')
        config.include('pyramid_jinja2')
        config.add_jinja2_renderer(".html")
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1',8000,app)
    server.serve_forever()