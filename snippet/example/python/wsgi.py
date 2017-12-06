
import logging
import routes
import webob.dec

LOG = logging.getLogger(__name__)


class Router(object):
    """WSGI middleware that maps incoming requests to WSGI apps."""

    def __init__(self, mapper):
        """Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        Examples:
          mapper = routes.Mapper()
          sc = ServerController()

          # Explicit mapping of one route to a controller+action
          mapper.connect(None, '/svrlist', controller=sc, action='list')

          # Actions are all implicitly defined
          mapper.resource('server', 'servers', controller=sc)

          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())
        """
        mapper.redirect("", "/")
        self._mapper = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, mapper)

    @webob.dec.wsgify
    def __call__(self, req):
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.
        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app


class Resource:
    def __init__(self, controller):
        self.controller = controller

    @webob.dec.wsgify
    def __call__(self, request):
        action_args = self._get_action_args(request.environ)
        action = action_args.pop('action', None)
        return self._process_stack(request, action, action_args, request.body)

    def _get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        if hasattr(self.controller, 'get_action_args'):
            return self.controller.get_action_args(request_environment)

        try:
            args = request_environment['wsgiorg.routing_args'][1].copy()
        except (KeyError, IndexError, AttributeError):
            return {}

        args.pop('controller', None)
        args.pop('format', None)

        return args

    def _process_stack(self, request, action, action_args, body):
        # Get the implementing method
        try:
            controller = self.controller if self.controller else self
            method = getattr(controller, action)
        except (AttributeError, TypeError):
            return webob.exc.HTTPNotFound()

        # Update the action args
        # contents = self.deserialize(body)
        # action_args.update(contents)

        # We don't handle the serialization.
        try:
            response = method(request, **action_args)
        except webob.exc.HTTPException as ex:
            response = ex
        except Exception as err:
            response = webob.exc.HTTPInternalServerError(err)
            LOG.error("Failed to handling %s: %s", request.path_qs, err)

        return response
