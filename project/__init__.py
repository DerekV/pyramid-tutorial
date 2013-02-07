from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from project.models import Base
from project.models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('usercreated', '/user-created', request_method='POST')
    config.add_route('createuser', '/create-user')
    config.scan()
    return config.make_wsgi_app()
