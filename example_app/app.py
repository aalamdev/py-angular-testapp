import json
import os
import webob.exc

from aalam_common.config import cfg
from aalam_common.redisdb import redis_conn
from aalam_common import wsgi
from aalam_common import auth
from aalam_common import role_mgmt
from aalam_common import sqa as zsqa
from aalam_common import CALLBACK_ROUTES, STATE_VALIDATION
from example_app.sqlalchemy import sqa, models


USE_REDISDB = True


def hook_entry(request):
    # We present different entry points
    # For admin user or users with Items/manage permisssion
    #    create form will be shown
    # For authenticated users who is not authorized enought to create
    #    items, can still access the items and items search page will
    #    shown
    # For the anonymous users, a general information will be shown

    if not auth.is_anonymous_user(request):
        return {"entry": "/aalam/py_ang_testapp/"}
    else:
        # anonymous users
        return {"entry": "/aalam/py_ang_testapp/s/templates/anon.html"}


class TestAppHandler(wsgi.BaseHandler):
    def __init__(self, mapper):
        # The BaseHandler.__init__ must be called with this mapper object.
        # If you do not have anything to do in this method, better not
        # define it.
        super(TestAppHandler, self).__init__(mapper)

    def send_angular_app(self, request, path_info):
        # We are not documenting this, as this API will be more useful
        # for the users than the developers.

        # We dont want to send the index page on a static prefixed URL, hence
        # we set the static_file attribute in the request object and let
        # the framework handle the response.

        # The index file will be placed by the aalam packager only if
        # it is mentioned in the setup.py like
        # setup(data_files=[("index.html", "resource/index.html"), ...])

        request.static_file = {"resource": "index.html",
                               "path": os.path.join(cfg.CONF.statics_dir,
                                                    "index.html")}

        # we are not returning any data, as the framework will take care
        # of it.

    def create_item_deserializer(self, request):
        # Input is expected to be either in json or xml format, so check
        # content type. json_deserializer() method is defined in the
        # BaseHandler, so using it as is.

        if request.content_type == "application/json":
            # We have an inbuilt json serializer defined in BaseHandler class
            return self.json_deserializer(request)
        elif request.content_type == "application/xml":
            # Parse the input xml data from request.body and return a
            # dictionary object
            pass

    def _redisify_item_key(self, name):
        return "example_app-%s" % name

    def create_item(self, request, name=None, type=None):
        """
        Create Item

        Creates a new item of a user chosen name and type

        Section:
            Items

        Input:
            type: application/json
            description: Input data in json
            spec:
                {
                    "name": "Some name",
                    "type": "Some type",
                }

        Input:
            type: application/xml
            description: Input data in xml
            spec:
                <item>
                    <name>Some name</name>
                    <type>Some type</type>
                </item

        Output:
            status_code: 200
            description: Successfully created a new item

        Output:
            status_code: 400
            description: Input data is wrong
        """

        # We documented this API and the documentation will be automatically
        # generated and be available in the public domain

        # validate the input data. The kwargs parmaters are the result from
        # deserializer, ie - create_item_deserializer()

        if not name or not type:
            raise webob.exc.HTTPBadRequest(
                explanation="Invalid input")

        # Get the email id of the user creating this item.
        user_email = auth.get_auth_user(request)

        # For future use, we store this item in redis.
        if USE_REDISDB:
            redis_conn.hmset(
                self._redisify_item_key(name),
                {"type": type, "owner": user_email})
        else:
            sqa.add_item(request.sqa_session, name, type, user_email)

        # If we return a tuple with null data, just the status code will
        # be set in the response.
        return (201, None)

    def get_item_serializer(self, data, response):
        # Data will be the data returned by get_item(). If the response output
        # is json, json_serializer from the base class will be automatically
        # used. This class is defined just for demonstration.

        # Set the respone content type
        response.content_type = "application/json"
        response.body = json.dumps(data)

    def get_item(self, request, item_name):
        # Document like above if you wish to expose this API in publicly

        # Note the parameter, 'item_name'. The name of the parameter is as
        # set in the URL for this action handler. The value will is as
        # it is in the actual path, example: for /aalam/testapp/some_name,
        # 'item_name' variable will have the value 'some_name'

        # We get the data back from redis and return a dictionary. This data
        # will be passed to get_item_serializer.
        if USE_REDISDB:
            return {"type": redis_conn.get(self._redisify_item_key(item_name))}
        else:
            return sqa.get_item(request.sqa_session, item_name)

    def get_items(self, request):
        # Document like above if you wish to expose this API in publicly

        if USE_REDISDB:
            ret = []
            for key in redis_conn.keys(self._redisify_item_key("*")):
                obj = redis_conn.hgetall(key)
                obj['name'] = key[len('example_app-'):]
                ret.append(obj)
            return ret
        else:
            # The request parameters can be accessed using request.params
            return sqa.get_items(request.sqa_session, request.params.copy())

    def update_item(self, request, item_name):
        # 'item_name' is set in the same way as it is for get_item.

        # we expect the new type in the request parameter. If not present
        # throw an error
        if 'type' not in request.params:
            raise webob.exc.HTTPBadRequest(explanation="Invalid usage")

        # Check if the owner of this item is updating this item. Else
        # throw an error.
        (user_email) = auth.get_auth_user(request)

        if USE_REDISDB:
            k = self._redisify_item_key(item_name)
            if redis_conn.hget(k,
                               "owner") != user_email:
                raise webob.exc.HTTPForbidden()

            # We can update the item now, as the user is verified.
            redis_conn.hset(k, "type", request.params['type'])
        else:
            sqa.update_item(
                request.sqa_session, item_name, request.params['type'],
                user_email)

        # This just sends a 200 OK response

    def delete_item(self, request, item_name):
        # 'item_name' is set in the same way as it is for get_item.

        # Check if the owner of this item is deleting this item. Else
        # throw an error.
        (user_email) = auth.get_auth_user(request)

        if USE_REDISDB:
            k = self._redisify_item_key(item_name)
            if redis_conn.hget(k, "owner") != user_email:
                raise webob.exc.HTTPForbidden()

            redis_conn.delete(k)
        else:
            sqa.delete_item(request.sqa_session, item_name, user_email)
        # This just sends a 200 OK response

    def get_user_permissions(self, request):
        # We have to send the permission that user possess for this app.
        (_, email) = auth.get_auth_user_id(request, deny_anon=False)

        # If the user is admin, he should have all the permissions as it is
        # not explicitly granted to the user.
        is_admin = role_mgmt.is_user_admin(email)

        # Check if the user has "Items/access" and "Items/manage" permissions.
        items_access = is_admin or \
            role_mgmt.is_client_authorized(request, "Items", "access")
        items_manage = is_admin or \
            role_mgmt.is_client_authorized(request, "Items", "manage")

        # This sends out a JSON content as the output. Our angular app
        # will be able to understand this output and construct the UI
        # appropriately.
        return {"items_manage": items_manage,
                "items_access": items_access}


def routes_cb(mapper):
    # We have the same handler for all the below urls. If not for submapper,
    # we will have to define 'handler' in each of the mapper.connect().
    # The mapper object has to be passed to the BaseHandler.__init__
    with mapper.submapper(handler=TestAppHandler(mapper)) as m:

        # Below url accepts input data, and it can be in xml/json format.
        # It allows only valid users with "Items/manage" permission
        m.connect("/aalam/py_ang_testapp/items",
                  action="create_item",
                  deserializer="create_item_deserializer",
                  permissions=role_mgmt.Permissions.all(
                      "Items/manage").deny_anon(),
                  conditions={"method": ['PUT']})

        # Below URL will send a json or XML output.
        # This api is denied for user who does not have "Items/access"
        # permission
        m.connect("/aalam/py_ang_testapp/item/{item_name}",
                  action="get_item",
                  permissions=role_mgmt.Permissions.all(
                    'Items/access'),
                  serializer="get_item_serializer",
                  conditions={"method": ['GET']})

        # Below URL will send the list of items create thus far
        m.connect("/aalam/py_ang_testapp/items",
                  action="get_items",
                  permissions=role_mgmt.Permissions.all(
                    'Items/access'),
                  conditions={'method': ["GET"]})

        # Below URL is used to update an items, but will permit a user
        # to update only if it is created by the same user.
        m.connect("/aalam/py_ang_testapp/item/{item_name}",
                  action="update_item",
                  permissions=role_mgmt.Permissions().deny_anon(),
                  conditions={"method": ['POST']})

        # Below URL is used to delete an item, but will permit a user
        # to delete only if it is created by the same user.
        m.connect("/aalam/py_ang_testapp/item/{item_name}",
                  action="delete_item",
                  permissions=role_mgmt.Permissions().deny_anon(),
                  conditions={"method": ['DELETE']})

        # Below url sends the permissions of the user to the angular app
        # So that it can disable or enable the necessary UI for a user.
        m.connect("/aalam/py_ang_testapp/user_permissions",
                  action="get_user_permissions",
                  conditions={'method': ['GET']})

        # Below url sends the index page. If there are any angular routes,
        # this will load the angular app and the angular framework will
        # route to the appropriate angular route
        # Notice the <base href="/aalam/py_ang_testapp/"> in the src/index.html
        m.connect("/aalam/py_ang_testapp/{path_info:.*}",
                  action="send_angular_app",
                  conditions={"method": ['GET']})


def entry(state):
    if state != STATE_VALIDATION:
        # do intializations here.
        zsqa.init_engine(models.db_name, models.Base)

    # entry point should return a list of callbacks. Since this is a
    # simple application, we just return a callback for routes.
    return {CALLBACK_ROUTES: routes_cb}
