from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.security import remember

from sqlalchemy.exc import DBAPIError

from project.models import DBSession
from project.models import User
from project.models import EventType
from project.models import Occurance

@view_config(route_name='home', renderer='templates/home.pt')
def rt_home(request):
    try:
        one = DBSession.query(User).filter(User.user_id == 'bob').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if 'userid' in request.POST:
        userid = request.params['userid']
        headers = remember(request,userid)
        return HTTPFound(
            location=request.route_url('home',
                                       username=userid),
            headers=headers)
    
    return {'logged_in': authenticated_userid(request) }

@view_config(route_name='user_created', renderer='templates/user_created.pt')
def rt_user_created(request):
   params = request.params
   userid = params['userid']

   try:
       one = DBSession.query(User).filter(User.user_id == 'bob').first()
   except DBAPIError:
       return Response(conn_err_msg, content_type='text/plain', status_int=500)

   user = User(userid)
   DBSession.add(user)

   return {'userid': userid, 'success': True, 'message': ""}

@view_config(route_name='create_user', renderer='templates/create_user.pt')
def rt_create_user(request):
   return {}

@view_config(route_name='event_type_created', renderer='templates/event_type_created.pt')
def rt_event_type_created(request):
   params = request.params
   description = params['description']

   et = EventType(description)
   session = DBSession()
   session.add(et)
   session.flush()
   event_code = et.eid 

   return {'description': description, 
           'success': True, 
           'message': "", 
           'event_code': event_code}

@view_config(route_name='create_event_type', renderer='templates/create_event_type.pt')
def rt_create_event_type(request):
   return {}

@view_config(route_name='event_type', renderer='templates/event_type.pt')
def rt_event_type(request):
    eid = request.matchdict['eventid']
    
    et = DBSession.query(EventType).get(eid)
    
    if 'userid' in request.POST:
        user_id = request.params['userid']
        observer = DBSession.query(User).filter(User.user_id==user_id).first()
        occurance = Occurance(observer, et)
        DBSession.add(occurance)

    count = len(et.occurances)

    return {'event_type_description': et.description, 
            'event_type_code': et.eid,
            'count':count,
            'logged_in': authenticated_userid(request)}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_project_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

