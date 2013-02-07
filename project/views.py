from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from project.models import DBSession
from project.models import User


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def rt_home(request):
    try:
        one = DBSession.query(User).filter(User.user_id == 'bob').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'project'}

@view_config(route_name='usercreated', renderer='templates/user_created.pt')
def rt_usercreated(request):
   params = request.params
   userid = params['userid']

   try:
       one = DBSession.query(User).filter(User.user_id == 'bob').first()
   except DBAPIError:
       return Response(conn_err_msg, content_type='text/plain', status_int=500)

   user = User(userid)
   DBSession.add(user);

   return {'userid': userid, 'success': True, 'message': ""}

@view_config(route_name='createuser', renderer='templates/create_user.pt')
def rt_createuser(request):
   return {}

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

