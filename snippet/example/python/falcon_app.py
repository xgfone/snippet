import logging
import traceback
import falcon

from falcon import routing

LOG = logging.getLogger("gunicorn.error")


class Application(falcon.API):
    __slots__ = ('_request_type', '_response_type',
                 '_error_handlers', '_media_type', '_router', '_sinks',
                 '_serialize_error', 'req_options', 'resp_options',
                 '_middleware', '_independent_middleware', '_router_search',
                 '_static_routes', "_resource")

    def __init__(self, *args, **kwargs):
        exc_handler = kwargs.pop("exception_handler", None)
        resource = kwargs.pop("resource", None)
        super(Application, self).__init__(*args, **kwargs)

        self._resource = resource
        if not exc_handler:
            exc_handler = self.__handle_exception

        self.add_error_handler(Exception, exc_handler)
        self.add_error_handler(falcon.HTTPError, self._http_error_handler)
        self.add_error_handler(falcon.HTTPStatus, self._http_status_handler)

    def __handle_exception(self, ex, req, resp, params):
        resp.status = falcon.HTTP_500
        resp.body = str(ex)
        LOG.error("Get an exception: method=%s, url=%s, err=%s", req.method, req.path, ex)
        LOG.error(traceback.format_exc())

    def add_route(self, uri_template, resource, *args, **kwargs):
        """Override the add_route in the parent class.

        Support:
            #### The original api.
            add_route("/path/to", resource)

            #### New APIs
            add_route("/path/to", resource, "resource_method", "GET")
            add_route("/path/to", resource, "resource_method", "GET", "POST")
            add_route("/path/to", resource, "resource_method", ["GET"])
            add_route("/path/to", resource, "resource_method", ["GET", "POST"])
            add_route("/path/to", resource, "resource_method", methods="GET")
            add_route("/path/to", resource, "resource_method", methods=["GET"])
            add_route("/path/to", resource, action="resource_method", methods="GET")
            add_route("/path/to", resource, action="resource_method", methods=["GET"])
            add_route("/path/to", None, action_func_or_method, "GET")
            add_route("/path/to", None, action_func_or_method, "GET", "POST")
            add_route("/path/to", None, action_func_or_method, ["GET", "POST"])
            add_route("/path/to", None, action=action_func_or_method, methods="GET")
            add_route("/path/to", None, action=action_func_or_method, methods=["GET", "POST"])
        """

        if not resource:
            resource = self._resource

        if args:
            action = args[0]
            methods = args[1:]
            if not methods:
                methods = kwargs["methods"]
        elif kwargs:
            action = kwargs["action"]
            methods = kwargs["methods"]
        elif resource:
            super(Application, self).add_route(uri_template, resource)
            return
        else:
            raise ValueError("Route arguments error")

        if not action:
            raise ValueError("action is empty")
        if not methods:
            raise ValueError("HTTP methods is empty")

        methods = methods if isinstance(methods, (list, tuple)) else [methods]
        if not callable(action):
            action = getattr(resource, action)

        method_map = {method.upper(): action for method in methods}
        routing.set_default_responders(method_map)
        self._router.add_route(uri_template, method_map, resource)
